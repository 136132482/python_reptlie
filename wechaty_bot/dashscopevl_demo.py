from http import HTTPStatus
import dashscope

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
    response = dashscope.MultiModalConversation.call(model='qwen-vl-plus',
                                                     messages=messages)
    # The response status_code is HTTPStatus.OK indicate success,
    # otherwise indicate request is failed, you can get error code
    # and message from code and message.
    if response.status_code == HTTPStatus.OK:
        print(response)
        return response['output']['choices'][0]['message']['content']
    else:
        message = 'Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message)
        print(message)
        raise ValueError(messages)

if __name__ == '__main__':
   reslut=simple_multimodal_conversation_call("https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fc-ssl.duitang.com%2Fuploads%2Fitem%2F202006%2F14%2F20200614204231_lxmif.thumb.1000_0.gif&refer=http%3A%2F%2Fc-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1706079952&t=99a2e7e1b836bd5a7887a719237bbf69"
                                        ,"描述一下这个表情,生成一个类似的表情文本")
   print(reslut)