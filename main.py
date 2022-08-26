import operator
import shlex
from subprocess import Popen, PIPE
import requests
from bs4 import BeautifulSoup

finaldict={}
ansdict={}


def p_format_d(sorted):
    for v in sorted.values():
        print("______________________________________________________________________")
        print("\n "+v)

def showans(url_list):

    for i in url_list:
        res=requests.get(i)
        soup=BeautifulSoup(res.text,"html.parser")
        ans=soup.select(".answercell")
        votes=soup.select(".answer")
        vts=votes[0].select_one('.js-vote-count').getText()
        #print("------------ANSWER--------------"+str(vts))
        answer= ans[0].select_one('.s-prose').getText()
        ansdict.update({(vts.strip()):answer})
    # print("Before SORTING")
    # print(ansdict)
    #sorted_dict={k:v for k,v in sorted(ansdict.items())}
    sorted_dict=dict(sorted(ansdict.items(), key=operator.itemgetter(0),reverse=True))
    # print("AFTER SORTNG")
    # print(sorted_dict)
    # finaldict.update(ansdict)
    p_format_d(sorted_dict)

def execute_and_return(cmd):
    args = shlex.split(cmd)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return out, err

def make_request(error):
    print("Searching for "+error)
    resp  = requests.get("https://api.stackexchange.com/"+"2.2/search?order=desc&tagged=python&sort=activity&intitle={}&site=stackoverflow".format(error))
    return resp.json()

def get_urls(json_dict):
    url_list = []
    count = 0
    for i in json_dict['items']:
        if i["is_answered"] and i["link"] not in url_list:
            url_list.append(i["link"])
        count+=1
        if count == len(i) or count == 3:
            break
    #print(url_list)

    #showans(url_list)
    # import webbrowser
    # for i in url_list:
    #     webbrowser.open(i)
    showans(url_list)

if __name__ == "__main__":
    out, err = execute_and_return("python test.py")
    error_message = err.decode("utf-8").strip().split("\r\n")[-1]
    # print(error_message)
    if error_message:

        filter_out = error_message.split(":")
        # print(filter_out)
        # print(filter_out[0])
        json1 = make_request(filter_out[0])
        json2 = make_request(filter_out[1])
        json = make_request(error_message)
        print("\n__________________________FETCHING SOLUTIONS______________________________\n")

        print("                   BEST SOLUTIONS FROM STACKOVERFLOW                          ")
        get_urls(json)
        get_urls(json2)
        get_urls(json1)

        # print(finaldict)
        #print(ansdict)

    else:
        print("No errors")
