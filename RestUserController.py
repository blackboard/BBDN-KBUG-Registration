import json
from cachetools import TTLCache
import requests
import datetime
import time
import ssl
import sys
import os
import urllib.parse

import Config



class RestUserController():
    target_url = ''

    def __init__(self, target_url, token):
        
        self.target_url = target_url
        self.token = token
        
        if Config.config['verify_certs'] == 'True':
            self.verify_certs = True
        else:
            self.verify_certs = False

        self.user_info = None

    def getUserInfo(self):
        return(self.user_info)

    def createLearnUser(self,user):
        endpoint = 'https://' + self.target_url + '/learn/api/public/v1/users'

        print('[User:createLearnUser()] token: ' + self.token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + self.token
        print('[User:createLearnUser()] authStr: ' + authStr)
        

        print("[User:createLearnUser()] POST Request URL: " + endpoint)
        print("[User:createLearnUser()] JSON Payload: NONE REQUIRED")
        r = requests.post(endpoint, json=user, headers={'Authorization':authStr, 'Content-Type' : 'application/json'},  verify=self.verify_certs)

        print("[User:createLearnUser()] STATUS CODE: " + str(r.status_code) )
        #print("[User:getUser()] RESPONSE:" + str(r.text))
        if r.status_code == 201 and r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
            return(res)
        elif r.status_code == 409:
            res = self.updateLearnUser(user)
            return(res)
        else:
            print("[User:getUser()] RESPONSE:" + str(r.text))
            return({ "http_status" : r.status_code, "result" : r.text })
    
    def updateLearnUser(self,user):
        endpoint = 'https://' + self.target_url + '/learn/api/public/v1/users/userName:' + user['userName']

        print('[User:createLearnUser()] token: ' + self.token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + self.token
        print('[User:createLearnUser()] authStr: ' + authStr)
        

        print("[User:createLearnUser()] POST Request URL: " + endpoint)
        print("[User:createLearnUser()] JSON Payload: NONE REQUIRED")
        r = requests.patch(endpoint, json=user, headers={'Authorization':authStr, 'Content-Type' : 'application/json'},  verify=self.verify_certs)

        print("[User:createLearnUser()] STATUS CODE: " + str(r.status_code) )
        #print("[User:getUser()] RESPONSE:" + str(r.text))
        if r.status_code == 200 and r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
            return(res)
        else:
            return({ "http_status" : r.status_code, "result" : r.text })

    def enrollUserInAllCourses(self, userId):
        
        for id in range(82,97):
            courseId = "_" + str(id) + "_1"
            
            endpoint = 'https://' + self.target_url + '/learn/api/public/v1/courses/' + courseId + '/users/' + userId

            print('[User:createLearnUser()] token: ' + self.token)
            #"Authorization: Bearer $token"
            authStr = 'Bearer ' + self.token
            print('[User:createLearnUser()] authStr: ' + authStr)
            
            payload = {
                "availability": {
                    "available": "Yes"
                },
                "courseRoleId": "Student"
            }

            print("[User:createLearnUser()] POST Request URL: " + endpoint)
            print("[User:createLearnUser()] JSON Payload: NONE REQUIRED")
            r = requests.put(endpoint, json=payload, headers={'Authorization':authStr, 'Content-Type' : 'application/json'},  verify=self.verify_certs)

            print("[User:createLearnUser()] STATUS CODE: " + str(r.status_code) )
            #print("[User:getUser()] RESPONSE:" + str(r.text))
            if r.status_code == 201 and r.text:
                res = json.loads(r.text)
                print(json.dumps(res,indent=4, separators=(',', ': ')))
            else:
                print("Error registering user <" + userId +"> for session <" + courseId + ">")

    def enrollUserInCourse(self, userId):
        
        courseId = "_866_1"
        
        endpoint = 'https://' + self.target_url + '/learn/api/public/v1/courses/' + courseId + '/users/' + userId

        print('[User:createLearnUser()] token: ' + self.token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + self.token
        print('[User:createLearnUser()] authStr: ' + authStr)
        
        payload = {
            "availability": {
                "available": "Yes"
            },
            "courseRoleId": "Student"
        }

        print("[User:createLearnUser()] POST Request URL: " + endpoint)
        print("[User:createLearnUser()] JSON Payload: NONE REQUIRED")
        r = requests.put(endpoint, json=payload, headers={'Authorization':authStr, 'Content-Type' : 'application/json'},  verify=self.verify_certs)

        print("[User:createLearnUser()] STATUS CODE: " + str(r.status_code) )
        #print("[User:getUser()] RESPONSE:" + str(r.text))
        if r.status_code == 201 and r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("[User:getUser()] RESPONSE:" + str(r.text))
            print("Error registering user <" + userId +"> for session <" + courseId + ">")


    def getUserInfoFromLearn(self):
        OAUTH_URL = 'https://' + self.target_url + '/learn/api/public/v1/users/me'

        print('[User:getUser()] token: ' + self.token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + self.token
        print('[User:getUser()] authStr: ' + authStr)
        

        print("[User:getUser()] GET Request URL: " + OAUTH_URL)
        print("[User:getUser()] JSON Payload: NONE REQUIRED")
        r = requests.get(OAUTH_URL, headers={'Authorization':authStr},  verify=self.verify_certs)

        print("[User:getUser()] STATUS CODE: " + str(r.status_code) )
        #print("[User:getUser()] RESPONSE:" + str(r.text))
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
            self.user_info = res
            return(self.user_info)
        else:
            print("NONE")