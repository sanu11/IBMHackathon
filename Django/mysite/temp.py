from ..mysite import email as em
mymail = em.Bimail('Sales email ' +datetime.now().strftime('%Y/%m/%d'), ['recipient1@gmail.com', 'recipient2@gmail.com'])
