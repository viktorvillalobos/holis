---
title: API Reference

language_tabs: # must be one of https://git.io/vQNgJ
  - javascript

toc_footers:
  - <a href='#'>Sign Up for a Developer Key</a>
  - <a href='https://github.com/slatedocs/slate'>Documentation Powered by Slate</a>

includes:
  - errors

search: true

code_clipboard: true
---

# Introduction

Welcome to Holis API documentation, Holis works with Rest and Socket services, you will find all relevant information here.

# Authentication

> To authorize, use this code:


```javascript
const kittn = require('kittn');

let api = kittn.authorize('meowmeowmeow');
```

> Make sure to replace `meowmeowmeow` with your API key.

Right now we are only supporting SESSION Authentication, you need to send the CSRF_TOKEN in all requests excepts in GET requests.


# Users

## Get All Users

```javascript

```

> The above command returns JSON structured like this:

```json
{
    "results": [
        {
            "avatar_thumb": "/media/avatars/jullshol.is_JxZGrOR.png",
            "birthday": "1995-08-15",
            "email": "julls@hol.is",
            "id": 2,
            "is_staff": true,
            "name": "Julls",
            "position": "Product Maker",
            "statuses": [
                {
                    "icon": "/media/%F0%9F%91%BB",
                    "icon_text": "",
                    "id": 8,
                    "is_active": false,
                    "text": "Absent"
                },
                {
                    "icon": "/media/%F0%9F%98%8B",
                    "icon_text": "",
                    "id": 7,
                    "is_active": false,
                    "text": "Having launch"
                },
                {
                    "icon": "/media/%F0%9F%A4%9D",
                    "icon_text": "",
                    "id": 6,
                    "is_active": false,
                    "text": "Metting"
                },
                {
                    "icon": "/media/%F0%9F%92%BB",
                    "icon_text": "",
                    "id": 5,
                    "is_active": true,
                    "text": "Available"
                }
            ],
            "username": "julls@hol.is"
        }
    ]
}
```

This endpoint retrieves all kittens.

### HTTP Request

`GET http://example.com/api/kittens`

### Query Parameters

Parameter | Default | Description
--------- | ------- | -----------
include_cats | false | If set to true, the result will also include cats.
available | true | If set to false, the result will include kittens that have already been adopted.

<aside class="success">
Remember — a happy kitten is an authenticated kitten!
</aside>

## Get a Specific Kitten

```ruby
require 'kittn'

api = Kittn::APIClient.authorize!('meowmeowmeow')
api.kittens.get(2)
```

```python
import kittn

api = kittn.authorize('meowmeowmeow')
api.kittens.get(2)
```

```shell
curl "http://example.com/api/kittens/2" \
  -H "Authorization: meowmeowmeow"
```

```javascript
const kittn = require('kittn');

let api = kittn.authorize('meowmeowmeow');
let max = api.kittens.get(2);
```

> The above command returns JSON structured like this:

```json
{
  "id": 2,
  "name": "Max",
  "breed": "unknown",
  "fluffiness": 5,
  "cuteness": 10
}
```

This endpoint retrieves a specific kitten.

<aside class="warning">Inside HTML code blocks like this one, you can't use Markdown, so use <code>&lt;code&gt;</code> blocks to denote code.</aside>

### HTTP Request

`GET http://example.com/kittens/<ID>`

### URL Parameters

Parameter | Description
--------- | -----------
ID | The ID of the kitten to retrieve

## Delete a Specific Kitten

```ruby
require 'kittn'

api = Kittn::APIClient.authorize!('meowmeowmeow')
api.kittens.delete(2)
```

```python
import kittn

api = kittn.authorize('meowmeowmeow')
api.kittens.delete(2)
```

```shell
curl "http://example.com/api/kittens/2" \
  -X DELETE \
  -H "Authorization: meowmeowmeow"
```

```javascript
const kittn = require('kittn');

let api = kittn.authorize('meowmeowmeow');
let max = api.kittens.delete(2);
```

> The above command returns JSON structured like this:

```json
{
  "id": 2,
  "deleted" : ":("
}
```

This endpoint deletes a specific kitten.

### HTTP Request

`DELETE http://example.com/kittens/<ID>`

### URL Parameters

Parameter | Description
--------- | -----------
ID | The ID of the kitten to delete

