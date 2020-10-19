import os

class EnvWrapper:
    def __init__(self):
        pass

    def input_func(self):
        self.input_checker = input()
        try:
            self.input_checker = str(self.input_checker)
        except:
            raise ValueError("Key of incorrect type.")
        return self.input_checker

    # Populates the keys into canvas.env permanently
    def populate_env(self):
        with open('canvas.env', 'w') as self.f:
            print("Enter Live Canvas Token: ")
            self.prod_token = "TOKEN="+str(self.input_func()+"\n")
            print("Enter Beta Canvas Token: ")
            self.beta_token = "BETA_TOKEN="+str(self.input_func()+"\n")
            self.f.write(self.prod_token)
            self.f.write(self.beta_token)

    # Brings canvas keys into virtual env during runtime
    def read_env(self):
        with open('canvas.env','r') as c:
            for line in c.readlines():
                try:
                    self.key,self.value = line.split('=')
                    os.putenv(self.key, self.value)
                except ValueError:
                    pass

    # Clear the contents of the canvas.env
    def clear_env(self):
        open('canvas.env', 'w').close()
