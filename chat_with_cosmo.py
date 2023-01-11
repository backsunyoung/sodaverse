import torch

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import colorful as cf
cf.use_true_colors()
cf.use_style('monokai')

import random

class CosmoAgent:
    def __init__(self):
        print(cf.bold | cf.purple("Loading COSMO-xl..."))
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained("allenai/cosmo-xl")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("allenai/cosmo-xl").to(self.device)
        self.conversation_history = []

    def observe(self, observation):
        self.conversation_history.append(observation)

    def set_input(self, situation_narrative="", role_instruction=""):
        input_text = " <turn> ".join(self.conversation_history)

        if role_instruction != "":
            input_text = "{} <sep> {}".format(role_instruction, input_text)

        if situation_narrative != "":
            input_text = "{} <sep> {}".format(situation_narrative, input_text)

        return input_text

    def generate(self, situation_narrative, role_instruction, user_response):

        self.observe(user_response)

        input_text = self.set_input(situation_narrative, role_instruction)

        inputs = self.tokenizer([input_text], return_tensors="pt").to(self.device)
        outputs = self.model.generate(inputs["input_ids"], max_new_tokens=128, temperature=1.0, top_p=.95, do_sample=True)
        cosmo_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)

        self.observe(cosmo_response)

        return cosmo_response

    def reset_history(self):
        self.conversation_history = []

    def run(self):
        def get_valid_input(prompt, default):
            while True:
                user_input = input(prompt)
                if user_input in ["Y", "N", "y", "n"]:
                    return user_input
                if user_input == "":
                    return default
        
        robot_name = input("당신의 로봇의 이름을 입력하세요")
        
         continue_chat = ""
            situation_narrative = input(cf.yellow("대화의 상황 설명/ 내러티브 입력 (비워 둘 수 있다):"))
            if situation_narrative == ("안녕" robot_name):
                situation_narrative = "로봇이 소환되었습니다."
        while True:
            continue_chat = ""
            situation_narrative = input(cf.yellow("대화의 상황 설명/ 내러티브 입력 (비워 둘 수 있다):"))
           
            role_instruction = input(cf.orange(robot_name"은 어떤 역할을 맡아야 할까요?" robot_name"은 누구와 이야기하고 있습니까 (비워 둘 수 있다):"))
            if role_instruction == "대화하자":
                role_instruction = "당신은" robot_name "이고 친구와 대화중입니다."
                
            if role_instruction == "몇살입니까"
            
                role_instruction = ""
                
                
             if role_instruction == "뭐하고 계십니까"
                role_instruction = ""
                
                
             if role_instruction == "식사는 하셨습니까"
                role_instruction = ""
                
                
              if role_instruction == "어떤 영화를 좋아합니까"
                role_instruction = ""
    
            self.chat(situation_narrative, role_instruction)
            continue_chat = get_valid_input(cf.purple("새 설정으로 새 대화를 시작하시겠습니까? [Y/N]:"), "Y")
            if continue_chat in ["N", "n"]:
                break
   
 else situation_narrative == "잘못된 입력입니다."
                
                
        print(cf.blue("다시 만나요"))

    def chat(self, situation_narrative, role_instruction):
        print(cf.green(robot_name "과 채팅! 대화 기록을 재설정하려면 [RESET]을 입력하고 대화를 종료하려면 [END]를 입력하세요"))
        while True:
            user_input = input("You: ")
            if user_input == "[RESET]":
                self.reset_history()
                print(cf.green("[대화 기록이 지워졌습니다. " robot_name "와/과 채팅하세요!]"))
                continue
            if user_input == "[END]":
                break
            response = self.generate(situation_narrative, role_instruction, user_input)
            print(cf.blue("Cosmo: " + response))

def main():
    print(cf.bold | cf.blue("환영합니다"))
    cosmo = CosmoAgent()
    cosmo.run()

if __name__ == '__main__':
   main()
