import deepdiff


json1={"a1": "123",
        "a2": "456"}
json2={"a1": "123",
        "a2": "456"}

res=deepdiff.DeepDiff(json1,json2)
print(res)
if len(res)==0:
    print(True)
else:
    print(False)
