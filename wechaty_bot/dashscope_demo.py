# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html
from http import HTTPStatus
import dashscope
dashscope.api_key="sk-2262f4bc3f1946038c0e8c62f197e577"


#通义千问
#a阿里云
def call_with_messages(msg):
    content={}
    messages=[]
    content['role']='user'
    content['content']=msg
    messages.append(content)
    # messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
    #             {'role': 'user', 'content': '如何做炒西红柿鸡蛋？'}]

    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
        return response['output']['choices'][0]['message']['content']
    else:
        message='Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message)
        print(message)
        raise ValueError(messages)






if __name__ == '__main__':
   message=call_with_messages()
   print(message)