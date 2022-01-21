Quick setup guide
=================

1.  .. image:: https://www.herokucdn.com/deploy/button.svg
        :alt: Deploy on Heroku
        :align: center
        :target: https://heroku.com/deploy

2.  (Optional) Customize the ``HERMOD_ADMIN_EMAIL`` variable with administrator email address
3.  Once deployed, set ``MAIL_USERNAME`` and ``MAIL_PASSWORD``variables to the values of ``MAILGUN_SMTP_LOGIN`` and ``MAILGUN_SMTP_PASSWORD``
4.  Go to ``/endpoint`` on your new Hermód instance and fill the form
5.  Look at application logs (or administrator mails if you set the variable)::

        Endpoint generated for contact@example.com from example.com:
        http://your-instance.herokuapp.com/QFnFLdnkPW0=/uc8RDeANub8NoSJfG0mYf3aXlg==/T84ffT6bhuNIag3Pb9rCyrVjKY39Hu5w5i9lu8SgpaQ=

6.  Set the generated endpoint adress as target for your form::

        <form
            action="http://your-instance.herokuapp.com/QFnFLdnkPW0=/uc8RDeANub8NoSJfG0mYf3aXlg==/T84ffT6bhuNIag3Pb9rCyrVjKY39Hu5w5i9lu8SgpaQ="
            method="POST">
            <p><input type="email" name="from" placeholder="Your email address"/></p>
            <p><textarea name="message" placehold="Your message"></textarea></p>
            <input type="hidden" name="redirect" value="http://domain.com/gotothispageaftersubmition"/>
            <input type="hidden" name="hermod" value=""/>
            <p><input type="submit" value="Send"></p>
        </form>

7.  You should now be ready to handle requests.

Command line tools
------------------

Generate AES and MAC keys:

    openssl rand -hex 16 | tee aes.key
    openssl rand -hex 16 | tee mac.key
    chmod go-rwx aes.key mac.key
