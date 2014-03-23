# Message Format

## Register

    From: <user>
    To: kaffee@example.com
    Subject: REGISTER
    
    Message:
    Name: <name>
    IBAN: <iban>
    BIC: <bic>

## Buying

    From: <user>
    To:   kaffee@example.com
    Cc:   <list of users>
    Subject: BUY
    
    Message:
    <list of products>
    <product a> OR <product b>
    </list of products>

### Parts

* `<user>` is one registered user
* `<list of users>` is a wrap-seperated list of `<user>`
* `<product a>` consists of `<qty> <name>`
* `<product b>` consists of `<qty> <name> <user>`

### Effects


* `<user>` and `<list of users>` get charged for every `<product a>` in `<list of products>`
* for every `<product b>` in `<list of products>` the according `<user>` gets charged the `<qty>` of `<name>` 



## Examples
### Adam buys himself one beer

    From: adam@fachschaft.tf
    To:   kaffee@fachschaft.tf
    Subject: BUY

    1 Beer


### Adam buys Eve and himself one beer

    From: adam@fachschaft.tf
    To:   kaffee@fachschaft.tf
    Cc:   eve@fachschaft.tf
    Subject: BUY

    1 Beer

### Adam buys Eve one beer

    From: adam@fachschaft.tf
    To:   kaffee@fachschaft.tf
    Subject: BUY

    1 Beer Eve
