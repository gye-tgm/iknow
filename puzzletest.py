def by8(s):
    out = []
    while len(s):
        out.insert(0, s[-8:])
        s = s[:-8]
    return out


page20 =     'ebPzGkMl56uEgmW6VndbErFuQElTtdjDDJKKIMEIq62aGrvgFGdCxiGDFQY2mqEt8e0Pdiaoc6llluG7FBerFXTaEYd0rgvv7YB3cMvJBv8FO8pj3qJ3quZJS3QEEIFBjEJVCqhCeEz3wgK3YuPrSTPXupLw30a9'
real_pages = 'Z5XMRsWfu8gbKtq8e925bxigjbfvA2p77CFFkWbkKvmJcGP9iR2V1JR7ijmatzbANZrX2J4dc8fffgRGiyZxi0v4bm2rxK66GmywcW6Cy6NihNHpwzCwzgBC3wjbbkiypbCeVzUVZbMwQKFwmgXx3vX0GHYQWR4D'


res = ''
for c in real_pages:
    if c not in page20:
        res += c
print(res)
print(''.join(set(res)))

page20 = by8(page20)
real_pages = by8(real_pages)

res = ''
for real_page, page20_page in zip(real_pages, page20):
    for c in page20_page:
        if c in real_page:
            res += c

print(len(res))
print(res)
