import asyncio

from comment import pyppeteer_demo

phone_url="https://www.eomsg.com/appweb/signIn.html"
async def  get_phone_number():
    page,brower=  await pyppeteer_demo.pyppeteer_test(phone_url)
    await page.type("#acct",'136132482')
    await page.type("#password","xiaohua1314")
    element=await page.xpath('//*[@id="app"]/div/section/div/div/form/div[3]/div/button')
    element=element[0]
    await element.click()
    await asyncio.sleep(5)
    page = (await brower.pages())[-1]
    html=await page.content()
    print(html)
    await page.type("#projectName","收短信")
    await page.waitFor('#gsdComboBox')
    elements=await page.querySelectorAll("select[id='gsdComboBox']")
    # selected_index = (await page.evaluate(""" el= > el.options[el.selectedIndex].value""")) - 1
    # selected_text = (await page.evaluateHandle("""(el)= > {
    # const options = Array.from (el.options);
    # return options[el.selectedIndex].innerText;}"""))
    await page.select("select[id='gsdComboBox']",'湖北')
    await page.waitFor('#yysComboBox')
    await page.select("select[id='yysComboBox']",'实卡')
    await page.type("#newPhoneNo",'1703857246604')
    await page.click("button[class='el-button el-button--primary']")


if __name__=="__main__":
    asyncio.get_event_loop().run_until_complete(get_phone_number())
