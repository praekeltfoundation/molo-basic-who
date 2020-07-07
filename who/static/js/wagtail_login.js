/* jshint esnext: true */
/*
This is a copy of the file below with the django admin login bits removed
https://github.com/AngellusMortis/django_microsoft_auth/blob/master/microsoft_auth/static/microsoft/js/login.js
*/
(function () {
    'use strict';

    class LoginController {
        constructor(options) {
            this._loginURL = options.authorization_url;
            this._loginWindow = null;

            // init event handlers
            document.getElementById('microsoft-login').addEventListener('click', this.handleMicrosoftLogin.bind(this));
            window.addEventListener('message', this.receiveMessage.bind(this));
        }

        // event handler to init Microsoft OAuth login window
        handleMicrosoftLogin(event) {
            // remove any existing errors first
            var error = document.querySelector('.errornote');

            if (error !== null) {
                error.parentNode.removeChild(error);
            }

            // close existing window if it exists
            if (this._loginWindow !== null) {
                this._loginWindow.close();
                this._loginWindow = null;
            }

            // open new login window
            this._loginWindow = window.open(
                this._loginURL,
                'microsoft-login',
                'height=560, width=790, left=550, top=200, menubar=no, location=no, resizable=no, scrollbars=yes, status=no, toolbar=no'
            );
        }

        // event handler to handle messages from child Microsoft login window
        receiveMessage(event) {
            if (event.origin === undefined) {
                event = event.originalEvent;
            }

            // verify the message is from us
            let origin = window.location.protocol + '//' + window.location
                .host;

            if (event.origin === origin) {
                if (event.data.microsoft_auth) {
                    let data = event.data.microsoft_auth;
                    if (data.error) {
                        console.warn(data);

                        // add error message to screen
                        var loginContainer = document.getElementById('content-main');
                        var error = document.createElement('p');

                        error.innerText = data.error_description;
                        error.className = 'errornote';

                        loginContainer.insertBefore(error,
                            loginContainer.firstChild);
                    } else {
                        // redirect to next URL if it was provided
                        let new_path = this.parseGETParam('next') || '/admin';

                        window.location = origin + new_path;
                    }
                }
            }
        }

        // parses GET parameter from URL
        parseGETParam(val) {
            let result = false;
            let tmp = [];
            let items = location.search.substr(1).split('&');

            for (let index = 0; index < items.length; index++) {
                tmp = items[index].split('=');

                if (tmp[0] === val) {
                    result = decodeURIComponent(tmp[1]);
                }
            }
            return result;
        }
    }

    window.microsoft = window.microsoft || {};
    window.microsoft.objects = window.microsoft.objects || {};
    window.microsoft.objects.LoginController = LoginController;
})();
