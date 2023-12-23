# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html
from urllib import request
import requests
from http import HTTPStatus
from wechaty_bot import  dashscope_demo
import dashscope
from dashscope.audio.asr import Recognition
import json
dashscope.api_key = 'sk-2262f4bc3f1946038c0e8c62f197e577'

r = requests.get(
    'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav'
)


def  change_voice():

    with open('asr_example.wav', 'wb') as f:
        f.write(r.content)
    recognition = Recognition(model='paraformer-realtime-v1',
                              format='wav',
                              sample_rate=16000,
                              callback=None)
    result = recognition.call('asr_example.wav')
    if result.status_code == HTTPStatus.OK:
        with open('asr_result.txt', 'w+') as f:
            for sentence in result.get_sentence():
                f.write(str(sentence) + '\n')
        print('Recognition done!')
        print(result['output']['sentence'][0]['text'])
        msg=result['output']['sentence'][0]['text']
        dashscope_demo.call_with_messages(msg)
    else:
        print('Error: ', result.message)


def  ansyn_change_voice():
    # For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html
    task_response = dashscope.audio.asr.Transcription.async_call(
        model='paraformer-v1',
        file_urls=[
            'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav',
            'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav'
        ])

    transcription_response = dashscope.audio.asr.Transcription.wait(
        task=task_response.output.task_id)

    if transcription_response.status_code == HTTPStatus.OK:
        for transcription in transcription_response.output['results']:
            url = transcription['transcription_url']
            result = json.loads(request.urlopen(url).read().decode('utf8'))
            print(json.dumps(result, indent=4, ensure_ascii=False))
        print('transcription done!')
    else:
        print('Error: ', transcription_response.output.message)



if __name__ == '__main__':
    ansyn_change_voice()
