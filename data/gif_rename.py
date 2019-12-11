from urllib import request


def save(terms):
    request.urlretrieve('https://giant.gfycat.com/%s.webm' % terms, '%s.webm' % terms)
    filename = '%s.webm' % terms
    return filename

save()