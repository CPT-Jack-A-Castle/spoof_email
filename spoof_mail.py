#!/usr/bin/python3
import os, sys, dns.resolver, telnetlib, time

def start():
    domain = sys.argv[1]
    check_mx(domain)

def check_mx(domain):
    d = []
    num = 0
    for x in dns.resolver.query(domain, 'MX'):
        d.append(x.to_text().split(' ')[1][:-1])

    if len(d) == 1:
        print('Using: %s' % d[0])
        message(d[0], domain)
    else:
        pass

    print('Found %i MX records\nPlease, select:' % len(d))

    for i in d:
        print('\t%i) %s' % (int(num), i))
        num +=1
    select = int(input('[#?]: '))
    try:
        s = d[int(select)]
        print('Using: %s' % s)
        message(s, domain)
    except Exception as e:
        print('[ERROR] Invalid option...')

def message(mx, domain):
    f = input('From (this can be anything): ')
    #f = 'info@microsoft.com'

    print('\nMust end with the same domain, ex: info@%s' % domain)
    to = input('To: ')
    #to = 'info@steuijt.nl'

    #title = input('Title: ')
    title = 'test'
    #body = 'test'
    global lines
    lines = []

    try:
        print('[Write the body] Finish with CTRL + C')
        while True:
            body = input('>>  ')
            lines.append(body)
    except KeyboardInterrupt:
        print('\n')
        print('[OK] Message')
        #for l in lines:
        #    print (l + '\n')
    send(mx, f, to, title)

def send(mx, f, to, title):
    bot = telnetlib.Telnet(mx, 25)
    bot.set_debuglevel(10)
    time.sleep(2)
    bot.write('EHLO '.encode('ascii') + mx.encode('ascii') + b'\n')
    time.sleep(2)
    bot.write('MAIL FROM: <'.encode('ascii') + f.encode('ascii') +  '>'.encode('ascii') + b'\n')
    time.sleep(2)
    bot.write('RCPT TO: <'.encode('ascii') + to.encode('ascii') +  '>'.encode('ascii') +  b'\n')
    time.sleep(2)

    bot.write('DATA'.encode('ascii') + b'\n')
    time.sleep(2)
    bot.write('Subject:'.encode('ascii') + title.encode('ascii') + b'\n')
    time.sleep(2)
    bot.write(b'\n')
    time.sleep(2)
    #bot.write(body.encode('ascii') + b'\n')
    for l in lines:
        bot.write(l.encode('ascii') + b'\n')
        time.sleep(2)
    time.sleep(2)
    bot.write('.'.encode('ascii') + b'\n')
    time.sleep(2)
    bot.write('QUIT'.encode('ascii'))
    time.sleep(2)
    print(bot.read_all())
    bot.close()
    print('\n[DONE] Message sent... Read the log to know if it ran into any errors, if not, the message should be sent successfuly.')
    print('[NOTE] Some spam-filters block these kind of messages so I cannot guarantee they received it.')
    sys.exit(0)


start()
