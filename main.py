try:
    import requests
except ModuleNotFoundError:
    print('Please install requests package.\nRefer this: https://pypi.org/project/requests/')
    exit()

MAX_SUGGESTIONS_PER_ERROR= 3

def bingSpellCheck(text):
    """
    Uses Bing Spell Check API v7.0
    :param text: input sentence
    :return: Corrected sentence
    """

    endpointURL = "https://api.cognitive.microsoft.com/bing/v7.0/spellcheck"
    bingSpellCheckAPIKey = "fac468a94e3a418f83d5dcbbbaa097fe"
    data = {
        "text": text,
    }
    params = {
        'mkt': 'en-us',
        'mode': 'proof'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Ocp-Apim-Subscription-Key': bingSpellCheckAPIKey,
    }
    response = requests.post(endpointURL, headers=headers, params=params, data=data)
    try:
        responseJSON = response.json()
        if responseJSON["flaggedTokens"]:
            offsetGenerated = 0
            for error in responseJSON["flaggedTokens"]:
                corrections = "/".join([word["suggestion"] for word in error["suggestions"]][:MAX_SUGGESTIONS_PER_ERROR])
                text = text[:error["offset"] + offsetGenerated] + corrections + text[error["offset"] + offsetGenerated +
                                                                                     len(error['token']):]
                offsetGenerated = len(corrections) - len(error['token'])
            return text
        else:
            return "No errors found, the input sentence is correct"
    except:
        return "Error message: Exception Handled"


def textGears(text):
    """
    Uses Text Gears API
    :param text: input sentence
    :return: Corrected sentence

    """

    endpointURL = "https://api.textgears.com/check.php"
    textGearsAPIKey = "M6oMDumysPaD5pX2"
    params = {
        "text": text,
        "key": textGearsAPIKey
    }

    response = requests.get(endpointURL, params=params)
    responseJSON = response.json()

    if responseJSON['result']:
        if responseJSON["errors"]:
            offsetGenerated = 0
            for error in responseJSON["errors"]:
                corrections = "/".join(error['better'][:MAX_SUGGESTIONS_PER_ERROR])
                text = text[:error["offset"] + offsetGenerated] + corrections + text[error["offset"] + offsetGenerated +
                                                                                     error['length']:]
                offsetGenerated = len(corrections) - error['length']
            return text
        else:
            return "No errors found, the input sentence is correct"
    else:
        return "Error code: {}\nError description: {}".format(responseJSON["error_code"], responseJSON["description"])


def virtualwritingtutor(text):
    """
    Uses Virtual Writing Tutor API

    :param text: input sentence
    :return: Corrected sentence
    """

    endpointURL = "https://virtualwritingtutor.com/api/checkgrammar.php"
    APIKey = "0688a721-f32b-11ea-883f-0cc47a352520"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        "text": text,
        "appKey": APIKey
    }

    response = requests.post(endpointURL, data=data, headers=headers)
    responseJSON = response.json()
    if responseJSON['status'] == "1":
        if responseJSON["error_grammar_count_total"]:
            offset = 0
            for error in responseJSON["check_grammar_feedback"]:
                corrections = "/".join(error["feedback_grammar_suggestion"][:MAX_SUGGESTIONS_PER_ERROR])
                wordOffset = text.find(error['error_grammar'])
                text = text[:wordOffset + offset] + corrections + text[wordOffset + len(error['error_grammar']):]
                offset = len(corrections) - wordOffset
            return text
        else:
            return "No errors found, the input sentence is correct"
    else:
        return "Error status: {}\nError message: {}".format(responseJSON["status"], responseJSON["message"])


if __name__ == "__main__":
    print('[NOTE] : The maximum suggestions per error is currently set to : {0}\n'.format(MAX_SUGGESTIONS_PER_ERROR))
    with open("sentences.txt", 'r', encoding="UTF-8") as file:
        sentences = file.readlines()

    for count, inputText in enumerate(sentences, start=1):
        inputText = inputText.strip()
        print("=" * 10, "Original Input # {0}".format(count),"=" * 10,"\n{0}".format(inputText))
        print("=" * 10, "TextGears API", "=" * 10, "\n{0}".format(textGears(inputText)))
        print("=" * 10, "Bing Spell Check API", "=" * 10, "\n{0}".format(bingSpellCheck(inputText)))
        print("=" * 10, "Virtual Writing Tutor API", "=" * 10, "\n{0}\n".format(virtualwritingtutor(inputText)))
