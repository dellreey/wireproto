import os,shutil,sys
shutil.copyfile(sys.argv[1],os.environ["WIREPROTO_OUTPUT"])
print(os.environ["WIREPROTO_PROMPT"][:160])
