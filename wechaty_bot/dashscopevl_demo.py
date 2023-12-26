from http import HTTPStatus
import random

import dashscope
from numba.np.numpy_support import is_array

dashscope.api_key="sk-2262f4bc3f1946038c0e8c62f197e577"

def simple_multimodal_conversation_call(imageurl,text):
    messages = [
        {
            "role": "user",
            "content": [
                {"image": imageurl},
                {"text": text}
            ]
        }
    ]
    response = dashscope.MultiModalConversation.call(model='qwen-vl-chat-v1',
                                                     top_k=50.0,
                                                     seed=random.randint(1000,10000),
                                                     messages=messages)
    # The response status_code is HTTPStatus.OK indicate success,
    # otherwise indicate request is failed, you can get error code
    # and message from code and message.
    if response.status_code == HTTPStatus.OK:
        print(response)
        text= response['output']['choices'][0]['message']['content']
        if type(text)==list:
           text= text[0]['text']
        return text
    else:
        message = 'Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message)
        print(message)
        # raise ValueError(messages)
        return "稍等一下，休息一下，服务器太辣鸡了，我处理不过来"

if __name__ == '__main__':
   reslut=simple_multimodal_conversation_call("https://3g79q59242.imdo.co/test_pic/123.gif"
                                        ,"描述一下照片的内容")
   print(reslut)