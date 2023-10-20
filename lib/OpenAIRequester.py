# Copyright 2023 Andy Curtis
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# The make_chat_completion_request and configure functions below were based upon
# the chat_completion.py in the https://github.com/richawo/chain-of-density github repo

from abc import ABC, abstractmethod
import openai
import time
import json

class OpenAIRequester(ABC):
    separator = "\n\n=====\n\n"

    def __init__(self, name, model, output_file):
        self.name = name
        self.model = model
        self.configure()
        self.system_message = None
        self.bad_message = None
        self.message = None
        self.output_file = output_file

    def close(self):
        self.output_file.close()

    @abstractmethod
    def get_system_message(self):
        pass

    @abstractmethod
    def get_user_message(self, input_text, warn=False):
        pass

    @abstractmethod
    def parse(self, input_text):
        pass

    # if the result of parse needs converted, overwrite this
    def format_output(self, parsed_text):
        return parsed_text

    def configure(
        self,
        temperature=1.0,
        top_p=1.0,
        n=1,
        stream=False,
        stop=None,
        max_tokens=None,
        presence_penalty=0,
        frequency_penalty=0,
        functions=[],
        function_call="auto"
    ):
        self.openai_parameters = {
            "model": self.model,
            "temperature": temperature,
            "top_p": top_p,
            "n": n,
            "stream": stream,
            "stop": stop,
            "max_tokens": max_tokens,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
        }

        if functions is not None and len(functions) > 0:
            self.openai_parameters["functions"] = functions
            self.openai_parameters["function_call"] = function_call

    def run(self, input_text):
        parameters = self.openai_parameters
        max_attempts = 90  # Maximum number of retry attempts
        retry_gap = 10.0  # Initial gap between retries in seconds
        bad_response = False
        content = None

        system_message = self.get_system_message()
        for attempt in range(max_attempts):
            try:
                parameters["messages"] = [system_message, self.get_user_message(input_text, bad_response)]
                completion = openai.ChatCompletion.create(**parameters)
                content = completion["choices"][0]["message"]["content"]
                resp = self.parse(content)
                if resp is not None:
                    output = self.format_output(resp)
                    self.save(output)
                    self.print(output)
                    return resp
                bad_response = True
            except Exception as e:
                print(f"Request failed on attempt {attempt + 1}. Error: {str(e)}")
                if attempt < max_attempts - 1:
                    retry_gap *= 1.5  # Increase the retry gap exponentially
                    if retry_gap > 600:
                        retry_gap = 600
                    time.sleep(retry_gap)

        return content  # If all retry attempts fail

    def save(self, output):
        if self.output_file is not None:
            self.output_file.write(output)
            self.output_file.write(OpenAIRequester.separator)
            self.output_file.flush()

    def print(self, output):
        print(self.name)
        print('')
        print(output)
        print(OpenAIRequester.separator)

    def parse_value_from_object(self, parsed, key):
        try:
            data = json.loads(parsed)
            if key in data:
                return data[key]
            else:
                print(parsed)
                print(f"{self.name}: {key} not found in JSON")
                return None
        except json.JSONDecodeError as e:
            print(f"{self.name}: JSON parsing error:", e)
            print(parsed)
            return None
        except Exception as e:
            print(f"{self.name}: An error occurred:", e)
            print(parsed)
            return None
        except:
            print(parsed)
            return None

    def parse_into_array(self, parsed, key):
        try:
            data = json.loads(parsed)
            if isinstance(data, list):
                res = []
                for item in data:
                    if key not in item:
                        print(parsed)
                        print(f"{self.name}: {key} not found in JSON")
                        print(item)
                        return None
                    res.append(item[key])
                return res
            else:
                if key not in data:
                    print(parsed)
                    print(f"{self.name}: {key} not found in JSON")
                    return None
                return [data[key]]
        except json.JSONDecodeError as e:
            print(f"{self.name}: JSON parsing error:", e)
            print(parsed)
            return None
        except Exception as e:
            print(f"{self.name}: An error occurred:", e)
            print(parsed)
            return None
        except:
            return None
