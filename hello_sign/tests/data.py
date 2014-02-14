# -*- coding: utf-8 -*-
import json
from collections import OrderedDict


HELLOSIGN_200_RESPONSE = json.dumps({   u'signature_request': {   u'cc_email_addresses': [],
                              u'custom_fields': [],
                              u'details_url': u'https://www.hellosign.com/home/manage?locate=79d41104dcf47068457c813615516f92c4ee6d63',
                              u'has_error': False,
                              u'is_complete': False,
                              u'message': u'This is a test singing please delete',
                              u'original_title': u'Test Signing',
                              u'requester_email_address': u'founders@lawpal.com',
                              u'response_data': [],
                              u'signature_request_id': u'79d41104dcf47068457c813615516f92c4ee6d63',
                              u'signatures': [   {   u'last_reminded_at': None,
                                                     u'last_viewed_at': None,
                                                     u'order': None,
                                                     u'signature_id': u'4555c5f356f8bdebb3bc7204d78af8ae',
                                                     u'signed_at': None,
                                                     u'signer_email_address': u'test+customer@lawpal.com',
                                                     u'signer_name': u'Test Customer',
                                                     u'status_code': u'awaiting_signature'},
                                                 {   u'last_reminded_at': None,
                                                     u'last_viewed_at': None,
                                                     u'order': None,
                                                     u'signature_id': u'a9c0ca82240d920c4303e5b56e2ad191',
                                                     u'signed_at': None,
                                                     u'signer_email_address': u'test+lawyer@lawpal.com',
                                                     u'signer_name': u'Test Tech Lawyer',
                                                     u'status_code': u'awaiting_signature'}],
                              u'signing_redirect_url': None,
                              u'signing_url': u'https://www.hellosign.com/editor/sign?guid=79d41104dcf47068457c813615516f92c4ee6d63',
                              u'subject': u'Test Signing',
                              u'test_mode': True,
                              u'title': u'/var/folders/nb/w1bxhlbd7jscn56p6gksdbcm0000gn/T/tmp7Xf1UC.docx'}})

#
# Dict Object representing the various types of HS webhook events
# 0. SIGNATURE_REQUEST_SENT - Sent to the registerd url when the intial request is setup
# 1. SIGNATURE_REQUEST_VIEWED_CLIENT - Customer has viewed the document
# 2. SIGNATURE_REQUEST_SIGNED_CLIENT - Sent when the client has signed the doc
# 3. SIGNATURE_REQUEST_VIEWED_LAWYER - Lawyer has viewed the document
# 4. SIGNATURE_REQUEST_SIGNED_LAWYER - Sent when the lawyer has signed the doc
# 5. SIGNATURE_REQUEST_ALL_SIGNED - Sent when all parties have signed
#
HELLOSIGN_WEBHOOK_EVENT_DATA = OrderedDict({"SIGNATURE_REQUEST_SENT": {
                                  "signature_request": {
                                    "test_mode": True,
                                    "cc_email_addresses": [],
                                    "custom_fields": [],
                                    "title": "#123455 Engagement Letter",
                                    "signature_request_id": "4092ab59cddab526ff79907f23f72022924617cc",
                                    "original_title": "Signature Request for #123455 Engagement Letter",
                                    "requester_email_address": "founders@lawpal.com",
                                    "details_url": "https://www.hellosign.com/home/manage?locate=4092ab59cddab526ff79907f23f72022924617cc",
                                    "signing_url": "https://www.hellosign.com/editor/sign?guid=4092ab59cddab526ff79907f23f72022924617cc",
                                    "has_error": False,
                                    "signatures": [
                                      {
                                        "signed_at": None,
                                        "status_code": "awaiting_signature",
                                        "last_viewed_at": None,
                                        "signer_email_address": "test+lawyer@lawpal.com",
                                        "signer_name": "Test Lawyer",
                                        "last_reminded_at": None,
                                        "signature_id": "5bf0117458c8e8fc76bd52e75f4b914b",
                                        "order": None
                                      },
                                      {
                                        "signed_at": None,
                                        "status_code": "awaiting_signature",
                                        "last_viewed_at": None,
                                        "signer_email_address": "test+customer@lawpal.com",
                                        "signer_name": "Test Customer",
                                        "last_reminded_at": None,
                                        "signature_id": "f8025d2899dfe85dba4db5b2083f1f54",
                                        "order": None
                                      }
                                    ],
                                    "response_data": [],
                                    "message": "Please review and sign this document at your earliest convenience",
                                    "is_complete": False,
                                    "signing_redirect_url": None,
                                    "subject": "Signature Request for #123455 Engagement Letter"
                                  },
                                  "account_guid": "295554d35f8ab1f3d7b9a276f439542868ac2b05",
                                  "event": {
                                    "event_hash": "df5b62ceaae857de1c51214dc89ea61e0ebf3994138b877b3ead2f888ca4feb3",
                                    "event_time": "1392037259",
                                    "event_type": "signature_request_sent",
                                    "event_metadata": {
                                      "reported_for_account_id": "295554d35f8ab1f3d7b9a276f439542868ac2b05"
                                    }
                                  },
                                  "client_id": "9bc892af173754698e3fa30dedee3826"
                                },

                                "SIGNATURE_REQUEST_VIEWED_CLIENT": {
                                  "signature_request": {
                                    "test_mode": True, 
                                    "cc_email_addresses": [], 
                                    "custom_fields": [], 
                                    "title": "#123455 Engagement Letter", 
                                    "signature_request_id": "5ba54718914ff7e6c615bb180f7635eebde59553", 
                                    "original_title": "Signature Request for #123455 Engagement Letter", 
                                    "requester_email_address": "founders@lawpal.com", 
                                    "details_url": "https://www.hellosign.com/home/manage?locate=5ba54718914ff7e6c615bb180f7635eebde59553", 
                                    "signing_url": None, 
                                    "has_error": False, 
                                    "signatures": [
                                      {
                                        "signed_at": None, 
                                        "status_code": "awaiting_signature", 
                                        "last_viewed_at": None, 
                                        "signer_email_address": "test+lawyer@lawpal.com", 
                                        "signer_name": "Test Lawyer", 
                                        "last_reminded_at": None, 
                                        "signature_id": "56637ef45e1899a25fb9d0bc4d51741d", 
                                        "order": None
                                      }, 
                                      {
                                        "signed_at": None, 
                                        "status_code": "awaiting_signature", 
                                        "last_viewed_at": 1392374943, 
                                        "signer_email_address": "test+customer@lawpal.com", 
                                        "signer_name": "Test Customer", 
                                        "last_reminded_at": None, 
                                        "signature_id": "6dfc33dafa56edfbd466a54f9ab6ab34", 
                                        "order": None
                                      }
                                    ], 
                                    "response_data": [], 
                                    "message": "Please review and sign this document at your earliest convenience", 
                                    "is_complete": False, 
                                    "signing_redirect_url": None, 
                                    "subject": "Signature Request for #123455 Engagement Letter"
                                  }, 
                                  "account_guid": "295554d35f8ab1f3d7b9a276f439542868ac2b05", 
                                  "event": {
                                    "event_hash": "7a7e08fc64b2739ff761cc563bf7f7affe813643694f7a932b64c8068a8b81cd", 
                                    "event_time": "1392374943", 
                                    "event_type": "signature_request_viewed", 
                                    "event_metadata": {
                                      "reported_for_account_id": "295554d35f8ab1f3d7b9a276f439542868ac2b05", 
                                      "reported_for_app_id": "9bc892af173754698e3fa30dedee3826", 
                                      "related_signature_id": ""
                                    }
                                  }, 
                                  "client_id": "9bc892af173754698e3fa30dedee3826"
                                },


                                "SIGNATURE_REQUEST_SIGNED_CLIENT": {
                                  "signature_request": {
                                    "custom_fields": [],
                                    "test_mode": True,
                                    "cc_email_addresses": [],
                                    "is_complete": False,
                                    "title": "#123455 Engagement Letter",
                                    "signature_request_id": "4092ab59cddab526ff79907f23f72022924617cc",
                                    "original_title": "Signature Request for #123455 Engagement Letter",
                                    "requester_email_address": "founders@lawpal.com",
                                    "details_url": "https://www.hellosign.com/home/manage?locate=4092ab59cddab526ff79907f23f72022924617cc",
                                    "signing_url": "https://www.hellosign.com/editor/sign?guid=4092ab59cddab526ff79907f23f72022924617cc",
                                    "has_error": False,
                                    "signatures": [
                                      {
                                        "signed_at": None,
                                        "status_code": "awaiting_signature",
                                        "last_viewed_at": None,
                                        "signer_email_address": "test+lawyer@lawpal.com",
                                        "signer_name": "Test Lawyer",
                                        "last_reminded_at": None,
                                        "signature_id": "5bf0117458c8e8fc76bd52e75f4b914b",
                                        "order": None
                                      },
                                      {
                                        "signed_at": 1392037300,
                                        "status_code": "signed",
                                        "last_viewed_at": None,
                                        "signer_email_address": "test+customer@lawpal.com",
                                        "signer_name": "Test Customer",
                                        "last_reminded_at": None,
                                        "signature_id": "f8025d2899dfe85dba4db5b2083f1f54",
                                        "order": None
                                      }
                                    ],
                                    "response_data": [
                                      {
                                        "value": None,
                                        "signature_id": "f8025d2899dfe85dba4db5b2083f1f54",
                                        "type": "signature",
                                        "name": None,
                                        "api_id": "d573df_2"
                                      }
                                    ],
                                    "message": "Please review and sign this document at your earliest convenience",
                                    "final_copy_uri": "/v3/signature_request/final_copy/4092ab59cddab526ff79907f23f72022924617cc",
                                    "signing_redirect_url": None,
                                    "subject": "Signature Request for #123455 Engagement Letter"
                                  },
                                  "account_guid": "295554d35f8ab1f3d7b9a276f439542868ac2b05",
                                  "event": {
                                    "event_hash": "2a8cb3bda7a7bf25d7865bb88af74f6002e07e5589c8fdb979a165232622c6bc",
                                    "event_time": "1392037300",
                                    "event_type": "signature_request_signed",
                                    "event_metadata": {
                                      "reported_for_account_id": "295554d35f8ab1f3d7b9a276f439542868ac2b05",
                                      "related_signature_id": "dab784c5c8cc8b67d46aeca6bf6e0e240c081f00"
                                    }
                                  },
                                  "client_id": "9bc892af173754698e3fa30dedee3826"
                                },


                                "SIGNATURE_REQUEST_VIEWED_LAWYER": {
                                  "signature_request": {
                                    "custom_fields": [], 
                                    "test_mode": True, 
                                    "cc_email_addresses": [], 
                                    "is_complete": False, 
                                    "title": "#123455 Engagement Letter", 
                                    "signature_request_id": "5ba54718914ff7e6c615bb180f7635eebde59553", 
                                    "original_title": "Signature Request for #123455 Engagement Letter", 
                                    "requester_email_address": "founders@lawpal.com", 
                                    "details_url": "https://www.hellosign.com/home/manage?locate=5ba54718914ff7e6c615bb180f7635eebde59553", 
                                    "signing_url": None, 
                                    "has_error": False, 
                                    "signatures": [
                                      {
                                        "signed_at": None, 
                                        "status_code": "awaiting_signature", 
                                        "last_viewed_at": 1392376819, 
                                        "signer_email_address": "test+lawyer@lawpal.com", 
                                        "signer_name": "Test Lawyer", 
                                        "last_reminded_at": None, 
                                        "signature_id": "56637ef45e1899a25fb9d0bc4d51741d", 
                                        "order": None
                                      }, 
                                      {
                                        "signed_at": 1392374955, 
                                        "status_code": "signed", 
                                        "last_viewed_at": 1392374943, 
                                        "signer_email_address": "test+customer@lawpal.com", 
                                        "signer_name": "Test Customer", 
                                        "last_reminded_at": None, 
                                        "signature_id": "6dfc33dafa56edfbd466a54f9ab6ab34", 
                                        "order": None
                                      }
                                    ], 
                                    "response_data": [
                                      {
                                        "value": None, 
                                        "signature_id": "6dfc33dafa56edfbd466a54f9ab6ab34", 
                                        "type": "signature", 
                                        "name": None, 
                                        "api_id": "9ed4ce_2"
                                      }
                                    ], 
                                    "message": "Please review and sign this document at your earliest convenience", 
                                    "final_copy_uri": "/v3/signature_request/final_copy/5ba54718914ff7e6c615bb180f7635eebde59553", 
                                    "signing_redirect_url": None, 
                                    "subject": "Signature Request for #123455 Engagement Letter"
                                  }, 
                                  "account_guid": "295554d35f8ab1f3d7b9a276f439542868ac2b05", 
                                  "event": {
                                    "event_hash": "3453b0e238db2699d969bee06c7e236b9ffb740e867aa96d7b94844c06819a88", 
                                    "event_time": "1392376819", 
                                    "event_type": "signature_request_viewed", 
                                    "event_metadata": {
                                      "reported_for_account_id": "295554d35f8ab1f3d7b9a276f439542868ac2b05", 
                                      "reported_for_app_id": "9bc892af173754698e3fa30dedee3826", 
                                      "related_signature_id": ""
                                    }
                                  }, 
                                  "client_id": "9bc892af173754698e3fa30dedee3826"
                                },

                                "SIGNATURE_REQUEST_SIGNED_LAWYER": {
                                  "signature_request": {
                                    "custom_fields": [],
                                    "test_mode": True,
                                    "cc_email_addresses": [],
                                    "is_complete": False,
                                    "title": "#123455 Engagement Letter",
                                    "signature_request_id": "4092ab59cddab526ff79907f23f72022924617cc",
                                    "original_title": "Signature Request for #123455 Engagement Letter",
                                    "requester_email_address": "founders@lawpal.com",
                                    "details_url": "https://www.hellosign.com/home/manage?locate=4092ab59cddab526ff79907f23f72022924617cc",
                                    "signing_url": "https://www.hellosign.com/editor/sign?guid=4092ab59cddab526ff79907f23f72022924617cc",
                                    "has_error": False,
                                    "signatures": [
                                      {
                                        "signed_at": 1392037626,
                                        "status_code": "signed",
                                        "last_viewed_at": None,
                                        "signer_email_address": "test+lawyer@lawpal.com",
                                        "signer_name": "Test Lawyer",
                                        "last_reminded_at": None,
                                        "signature_id": "5bf0117458c8e8fc76bd52e75f4b914b",
                                        "order": None
                                      },
                                      {
                                        "signed_at": 1392037300,
                                        "status_code": "signed",
                                        "last_viewed_at": None,
                                        "signer_email_address": "test+customer@lawpal.com",
                                        "signer_name": "Test Customer",
                                        "last_reminded_at": None,
                                        "signature_id": "f8025d2899dfe85dba4db5b2083f1f54",
                                        "order": None
                                      }
                                    ],
                                    "response_data": [
                                      {
                                        "value": None,
                                        "signature_id": "f8025d2899dfe85dba4db5b2083f1f54",
                                        "type": "signature",
                                        "name": None,
                                        "api_id": "d573df_2"
                                      },
                                      {
                                        "value": "IP: 91.61.209.147",
                                        "signature_id": "f8025d2899dfe85dba4db5b2083f1f54",
                                        "type": None,
                                        "name": None,
                                        "api_id": "c6936e_1"
                                      },
                                      {
                                        "value": "Time: February 10th, 2014 1:01 PM UTC",
                                        "signature_id": "f8025d2899dfe85dba4db5b2083f1f54",
                                        "type": None,
                                        "name": None,
                                        "api_id": "c6936e_2"
                                      },
                                      {
                                        "value": None,
                                        "signature_id": "5bf0117458c8e8fc76bd52e75f4b914b",
                                        "type": "signature",
                                        "name": None,
                                        "api_id": "d573df_1"
                                      }
                                    ],
                                    "message": "Please review and sign this document at your earliest convenience",
                                    "final_copy_uri": "/v3/signature_request/final_copy/4092ab59cddab526ff79907f23f72022924617cc",
                                    "signing_redirect_url": None,
                                    "subject": "Signature Request for #123455 Engagement Letter"
                                  },
                                  "account_guid": "295554d35f8ab1f3d7b9a276f439542868ac2b05",
                                  "event": {
                                    "event_hash": "5781e24900fedc43259d528cb7bff68ea1b41f95fef356a0400a7c5a1fb9fc20",
                                    "event_time": "1392037626",
                                    "event_type": "signature_request_signed",
                                    "event_metadata": {
                                      "reported_for_account_id": "295554d35f8ab1f3d7b9a276f439542868ac2b05",
                                      "related_signature_id": "d7f7c3562903d04830630023faf628285892a6ae"
                                    }
                                  },
                                  "client_id": "9bc892af173754698e3fa30dedee3826"
                                },


                                "SIGNATURE_REQUEST_ALL_SIGNED": {
                                  "signature_request": {
                                    "custom_fields": [],
                                    "test_mode": True,
                                    "cc_email_addresses": [],
                                    "is_complete": True,
                                    "title": "#123455 Engagement Letter",
                                    "signature_request_id": "4092ab59cddab526ff79907f23f72022924617cc",
                                    "original_title": "Signature Request for #123455 Engagement Letter",
                                    "requester_email_address": "founders@lawpal.com",
                                    "details_url": "https://www.hellosign.com/home/manage?locate=4092ab59cddab526ff79907f23f72022924617cc",
                                    "signing_url": "https://www.hellosign.com/editor/sign?guid=4092ab59cddab526ff79907f23f72022924617cc",
                                    "has_error": False,
                                    "signatures": [
                                      {
                                        "signed_at": 1392037626,
                                        "status_code": "signed",
                                        "last_viewed_at": None,
                                        "signer_email_address": "test+lawyer@lawpal.com",
                                        "signer_name": "Test Lawyer",
                                        "last_reminded_at": None,
                                        "signature_id": "5bf0117458c8e8fc76bd52e75f4b914b",
                                        "order": None
                                      },
                                      {
                                        "signed_at": 1392037300,
                                        "status_code": "signed",
                                        "last_viewed_at": None,
                                        "signer_email_address": "test+customer@lawpal.com",
                                        "signer_name": "Test Customer",
                                        "last_reminded_at": None,
                                        "signature_id": "f8025d2899dfe85dba4db5b2083f1f54",
                                        "order": None
                                      }
                                    ],
                                    "response_data": [
                                      {
                                        "value": None,
                                        "signature_id": "f8025d2899dfe85dba4db5b2083f1f54",
                                        "type": "signature",
                                        "name": None,
                                        "api_id": "d573df_2"
                                      },
                                      {
                                        "value": "IP: 91.61.209.147",
                                        "signature_id": "f8025d2899dfe85dba4db5b2083f1f54",
                                        "type": None,
                                        "name": None,
                                        "api_id": "c6936e_1"
                                      },
                                      {
                                        "value": "Time: February 10th, 2014 1:01 PM UTC",
                                        "signature_id": "f8025d2899dfe85dba4db5b2083f1f54",
                                        "type": None,
                                        "name": None,
                                        "api_id": "c6936e_2"
                                      },
                                      {
                                        "value": None,
                                        "signature_id": "5bf0117458c8e8fc76bd52e75f4b914b",
                                        "type": "signature",
                                        "name": None,
                                        "api_id": "d573df_1"
                                      },
                                      {
                                        "value": "IP: 91.61.209.147",
                                        "signature_id": "5bf0117458c8e8fc76bd52e75f4b914b",
                                        "type": None,
                                        "name": None,
                                        "api_id": "578aad_1"
                                      },
                                      {
                                        "value": "Time: February 10th, 2014 1:07 PM UTC",
                                        "signature_id": "5bf0117458c8e8fc76bd52e75f4b914b",
                                        "type": None,
                                        "name": None,
                                        "api_id": "578aad_2"
                                      }
                                    ],
                                    "message": "Please review and sign this document at your earliest convenience",
                                    "final_copy_uri": "/v3/signature_request/final_copy/4092ab59cddab526ff79907f23f72022924617cc",
                                    "signing_redirect_url": None,
                                    "subject": "Signature Request for #123455 Engagement Letter"
                                  },
                                  "account_guid": "295554d35f8ab1f3d7b9a276f439542868ac2b05",
                                  "event": {
                                    "event_hash": "0fa5ca7618dfe80d2fb6207b21b82ca2023331c1b776b40872cc832b902c3bdb",
                                    "event_time": "1392037626",
                                    "event_type": "signature_request_all_signed",
                                    "event_metadata": {
                                      "reported_for_account_id": "295554d35f8ab1f3d7b9a276f439542868ac2b05"
                                    }
                                  },
                                  "client_id": "9bc892af173754698e3fa30dedee3826"
                                }
                              })


SIGNATURE_URL_REQUEST = {'embedded': {
                          'sign_url': 'https://www.hellosign.com/editor/embeddedSign?signature_id={signature_id}&token={token}',
                          'expires_at': 1392110915
                        }}
