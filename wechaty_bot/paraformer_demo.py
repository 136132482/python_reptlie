# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html
import asyncio
from urllib import request
import requests
from http import HTTPStatus
from wechaty_bot import  dashscope_demo
import dashscope
from dashscope.audio.asr import Recognition
import json
dashscope.api_key = 'sk-2262f4bc3f1946038c0e8c62f197e577'

# r = requests.get(
#     'F:\\test_voice\\audio.wav'
# )


#paraformer-mtl-v1 模型 录音文件识别
def  change_voice(path):
    # with open(path, 'wb') as f:
    #     f.write(r.content)
    recognition = Recognition(model='paraformer-realtime-v1',
                              format='wav',
                              sample_rate=16000,
                              callback=None)
    result = recognition.call(path)
    if result.status_code == HTTPStatus.OK:
        with open('asr_result.txt', 'w+') as f:
            for sentence in result.get_sentence():
                f.write(str(sentence) + '\n')
        print('Recognition done!')
        print(result['output']['sentence'][0]['text'])
        msg=result['output']['sentence'][0]['text']
        return msg
    else:
        message = 'Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            result.request_id, result.status_code,
            result.code, result.message)
        print(message)
        raise ValueError(message)





#paraformer-v1 准确率高  paraformer-mtl-v1 可识别方言
def  ansyn_change_voice(file_urls):
    # For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html
    task_response = dashscope.audio.asr.Transcription.async_call(
        model='paraformer-mtl-v1',
        file_urls=file_urls
    )
    transcription_response = dashscope.audio.asr.Transcription.wait(
        task=task_response.output.task_id)
    msg_list=[]
    if transcription_response.status_code == HTTPStatus.OK:
        for transcription in transcription_response.output['results']:
            url = transcription['transcription_url']
            result = json.loads(request.urlopen(url).read().decode('utf8'))
            print(json.dumps(result, indent=4, ensure_ascii=False))
            # result=json.dumps(result, indent=4, ensure_ascii=False)
            msg=result['transcripts'][0]['text']
            msg_list.append(msg)
        return "".join(msg_list)
        print('transcription done!')
    else:
        message = 'Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            transcription_response.request_id, transcription_response.status_code,
            transcription_response.code, transcription_response.message)
        print(message)
        raise ValueError(message)



if __name__ == '__main__':
    # msg=change_voice('F:\\test_voice\\audio.wav')
    # print(dashscope_demo.call_with_messages(msg))
    file_url=[]
    file_url.append("https://3g79q59242.imdo.co/audio.mp3")
    msg= ansyn_change_voice(file_url)
    print(dashscope_demo.call_with_messages(msg))