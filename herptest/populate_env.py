import os

def input_func():
    test = input()
    try:
        test = str(test)
    except:
        raise ValueError("Key of incorrect type.")
    return test

# Populates the keys into canvas.env permanently
def populate_env():
    with open('canvas.env', 'w') as f:
        prod_token = "TOKEN="+str(input_func()+"\n")
        beta_token = "BETA_TOKEN="+str(input_func()+"\n")
        f.write(prod_token)
        f.write(beta_token)

# Brings canvas keys into virtual env during runtime
def read_env():
    with open('canvas.env','r') as c:
        for line in c.readlines():
            try:
                key,value = line.split('=')
                os.putenv(key, value)
            except ValueError:
                pass

# Clear the contents of the canvas.env
def clear_env():
    open('canvas.env', 'w').close()


# Test Main - Temp
def main():
    populate_env()
    
if __name__ == "__main__":
    main()
