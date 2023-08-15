# app.py

# Reference: You can find the source code in :
# 1: CV: https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library-40?tabs=visual-studio%2Clinux&pivots=programming-language-python
# 2: Text Analysis: https://learn.microsoft.com/en-us/python/api/overview/azure/ai-textanalytics-readme?view=azure-python
# 3: Language & Speech: https://learn.microsoft.com/en-us/training/modules/translate-speech-speech-service/5-exercise-translate-speech?ns-enrollment-type=learningpath&ns-enrollment-id=learn.wwl.process-translate-speech-azure-cognitive-speech-services


from flask import Flask, render_template, request, send_file
########## Quiz1: Please import azure ai vision package as sdk
# import ??????????
from azure.core.credentials import AzureKeyCredential

########## Quiz2: Please find Text Analysis of "Multiple Analysis" section to find the package
from azure.ai.textanalytics import (
    TextAnalyticsClient,
    # ????
    AnalyzeSentimentAction,
)
import azure.cognitiveservices.speech as speech_sdk
import json
import os
import copy

app = Flask(__name__)

########## Quiz3: Please enter your endpoint, key and region

COG_ENDPOINT='Your cognitive serviceendpoint'
COG_KEY='Your cognitive service key'
COG_REGION='Your cognitive region'
uploaded_count = 0  # Initialize the uploaded count
CV_data = []



@app.route('/')
def index():
    return render_template('test.html')

@app.route('/image_processing', methods=['POST'])
def image_processing():
    global uploaded_count  
    image = request.files['image']
    uploaded_count += 1  
    unique_filename = 'temp_image'+str(uploaded_count)+'.png'

    image.save(unique_filename)
    return_val = CVDetect(unique_filename)
    return json.dumps(return_val)

@app.route('/nlp_processing', methods=['POST'])
def nlp_processing():
    global CV_data 

    text = ''
    for i in CV_data:
	    text = text + i + ' '
    result_collector = NLP(text)
    # return json.dumps(return_val)

    return json.dumps(result_collector)
	

@app.route('/speech_processing', methods=['POST'])
def speech_processing():
    data = request.get_json()
    selected_value = data.get('selectedValue')

    global CV_data
    text_total = ''
    for i in CV_data:
        text_total = text_total + ' ' + i 
    if selected_value == "en-US to zh-TW":
        result = ENGUStoZHTW(text_total)
    elif selected_value == "zh-TW to en-US":
        result = ZHTWtoENGUS(text_total)

    return json.dumps({'translate_result': result})

@app.route('/get_wav_file')
def get_wav_file():
    wav_file_path = 'output.wav'
    return send_file(wav_file_path, mimetype='audio/wav')


def CVDetect(filename):
    global CV_data 
    global COG_ENDPOINT
    global COG_KEY
    
    CV_data = []
    service_options = sdk.VisionServiceOptions(COG_ENDPOINT, COG_KEY)
    vision_source = sdk.VisionSource(filename=filename)

    analysis_options = sdk.ImageAnalysisOptions()

########## Quiz4: Please setting the analysis_options

    analysis_options.features = (
        # ???
        # ???
    )

    # ???

    # ???

    image_analyzer = sdk.ImageAnalyzer(service_options, vision_source, analysis_options)

    result = image_analyzer.analyze()
    return_value = ['', []]
    if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:

        if result.caption is not None:
            print(" Caption:", result.caption.content)
            return_value[0] = result.caption.content
        if result.text is not None:
            print(" Text:")
            for line in result.text.lines:
                points_string = "{" + ", ".join([str(int(point)) for point in line.bounding_polygon]) + "}"
                print("   Line: '{}', Bounding polygon {}".format(line.content, points_string))
                return_value[1].append(line.content)
                CV_data.append(line.content)

    return {'caption': return_value[0], 'text': return_value[1]}

def NLP(text):

	global COG_ENDPOINT
	global COG_KEY
########## Quiz5: Please create a TextAnalyticsClient()

	# ???

	documents = [text]
	poller = text_analytics_client.begin_analyze_actions(
		documents,
		display_name="Sample Text Analysis",
		actions=[
########## Quiz6: Please enter actions here

			# ???
			# ???
			# ???
			# ???
		],
	)

	document_results = poller.result()
	result_collector = []
	sentiment_collector = []

	for doc, action_results in zip(documents, document_results):
		print(f"\nDocument text: {doc}")
		for result in action_results:


			if result.kind == "EntityLinking":
########## Quiz7: Please complete the for loop to continue.

				# for ???
					print(f"......Entity name: {linked_entity.name}")
					print(f".........Data source language: {linked_entity.language}")
					print(f".........Data source URL: {linked_entity.url}")
					print(".........Document matches:")
					result_collector.append('▪️&nbsp' + 'Entity:&nbsp' + str(linked_entity.name) )
					result_collector.append('&nbsp&nbsp' + 'Language:&nbsp' + str(linked_entity.language) )
					result_collector.append('&nbsp&nbsp' + 'URL:&nbsp<a href="' + str(linked_entity.url) + '">' + str(linked_entity.url) + '</a>' )
					result_collector.append( '' )


				

			if result.kind == "SentimentAnalysis":
				print("...Results of Analyze Sentiment action:")
				print(f"......Overall sentiment: {result.sentiment}")
				sentiment_collector.append('&nbsp&nbsp&nbsp&nbsp' + 'Sentiment:&nbsp' + str(result.sentiment))
				print(
					f"......Scores: positive={result.confidence_scores.positive}; \
					neutral={result.confidence_scores.neutral}; \
					negative={result.confidence_scores.negative} \n"
				)
				sentiment_collector.append('&nbsp&nbsp&nbsp&nbsppositive:&nbsp' + str(result.confidence_scores.positive))
########## Quiz8: Please continue append neutral and negative into sentiment_collector

				# ??? 
				# ??? 



		return {'nlp_result': result_collector, 'sentiment_result': sentiment_collector}

def ZHTWtoENGUS(sentence=''):
    if sentence != '':
        Syntthesize(sentence, 'zh-Hant', filename='input.wav')
        return Translate(sourceLanguage='zh-CN', targetLanguage='en')
    else:
        print('Not implement')



def ENGUStoZHTW(sentence=''):
    if sentence != '':
        Syntthesize(sentence, 'en-us', filename='input.wav')
        return Translate(sourceLanguage='en-US', targetLanguage='zh-Hant')
    else:
        print('Not implement')


def Syntthesize(text, targetLanguage, filename):
    global speech_config
    global translation_config
    global COG_KEY
    global COG_REGION

    speech_config = speech_sdk.SpeechConfig(COG_KEY, COG_REGION)
    # https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=speech-translation
    # Synthesize translation
    voices = {
            "zh-Hant": "zh-TW-YunJheNeural",
            "en-us": "en-US-AmberNeural"
    }
    speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    speak = speech_synthesizer.speak_text_async(text).get()
    if speak.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted:
        audio_file_path = filename
        with open(audio_file_path, "wb") as audio_file:
            audio_file.write(speak.audio_data)
        print("Audio saved to:", audio_file_path)
    else:
        print(speak.reason)





def Translate(sourceLanguage, targetLanguage):
########## Quiz9: Please declare the following four global variables: "speech_config", "translation_config", "COG_KEY", and "COG_REGION".
    # ??? 
    # ??? 

    # ???
    # ???

    # Configure translation
    translation_config = speech_sdk.translation.SpeechTranslationConfig(COG_KEY, COG_REGION)
    translation_config.speech_recognition_language = sourceLanguage
    translation_config.add_target_language(targetLanguage)

    # Configure speech
    speech_config = speech_sdk.SpeechConfig(COG_KEY, COG_REGION)
    translation = ''

    # Translate speech
    audioFile = 'input.wav'
    # playsound(audioFile)
    audio_config = speech_sdk.AudioConfig(filename=audioFile)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config)
    print("Getting speech from file...")
    result = translator.recognize_once_async().get()
    print('Translating "{}"'.format(result.text))
    print(result.translations)
    translation = result.translations[targetLanguage]
    if targetLanguage == 'en':
        Syntthesize(translation, 'en-us', filename='output.wav')
    elif targetLanguage == 'zh-Hant':
        Syntthesize(translation, 'zh-Hant', filename='output.wav')



    return translation

if __name__ == '__main__':
     
    # Quiz10: To execute the app, run app.run() here and specify the host as '0.0.0.0' and the port as 5000.
    # ???
