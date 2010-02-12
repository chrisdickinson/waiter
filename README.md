Waiter
======

    ``There's a hair in my soup!''

Waiter is a [Dolt](http://www.github.com/tswicegood/Dolt)-inspired API wrapper. Like Dolt, it overloads one of the existing
operators to do it's dirty work. Unlike Dolt, the operator it overrides doesn't drive IPython absolutely crazy :)

A simple example:

    from waiter import Waiter
    waiter = Waiter()
    waiter/"https://twitter.com/users/show.json"/{
        'screen_name':'isntitvacant',
    }
    #-> outputs a bunch of data from twitter

Or if you want to go piecewise:

    from waiter import Waiter
    waiter = Waiter()
    waiter/"https://twitter.com"
    waiter/"users"
    waiter/"show.json"
    waiter/{
        'screen_name':'isntitvacant',
    }
    #-> outputs a bunch of data from twitter

And Waiter will be smart enough to insert the appropriate slashes. \(The rule is: for the first string, don't infix any slashes,
and afterwards prepend a slash to every divided string\).

But wait!
---------

The restaurant-themed analogies don't stop there! Waiter delegates to a Chef object to help it prepare a tasty HttpRequest meal.
The Chef is responsible for cooking the Waiter's "order" -- the stack of strings the waiter produces -- and the Waiter's "payload"
-- the keyword arguments that go into GET or POST. He's also got the heady task of telling the Waiter when an order just
doesn't make sense. He can assign errors, and the Waiter will diligently raise an error to you, the customer, detailing just what
went wrong, in the form of a `Waiter.Error` exception.

When a Waiter is taking an order, he doesn't much care what he's writing down, really. It just needs to be a value. It's not
up to him what he'll listen to! He just needs to look up what to do on his `Menu`. When you send a `Waiter` out into the world,
he'll bring the trusty default menu with him -- it's what tells him how to accept `str` and `dict` orders. But if you want to
get him to accept something else without a fuss, you'll want to provide him a different `menu_class` to work with:

    class HttpMenu(Menu):
        def take_a_http_thing(self, waiter):
            waiter._http = self.value

        def __init__(self, *args, **kwargs):
            kwargs.update({
                'dispatch_update':{
                    httplib2.Http:self.take_a_http_thing
                }
            })
            return super(HttpMenu, self).__init__(*args, **kwargs)

    waiter = Waiter(menu_class=HttpMenu)
    http = httplib2.Http()
    
    waiter/http
    waiter._http is http        # -> True

But wait! Again! What if you want something to _always_ be on the menu? What if there's some tasty treat you just *cannot do without*.
What if... _you want more restaurant themed puns_?

    # don't worry, I got you

    class Arrabbiata(object):
        """
            arrabbiata is ALWAYS on the menu.
        """
        def accept_waiter(self, waiter):
            return "delicious!"

    waiter = Waiter()       # nothing up my sleeves!
    tasty_pasta = Arrabbiata()
    print waiter/tasty_pasta        # -> "delicious!"

The default Chef is very permissive -- he'll cook just about anything! But the functionality is there to create Chefs who only
follow predetermined recipes. Or even Chefs that insert their own ingredients -- a TwitterChef who always pushes in the url
"https://twitter.com" when your waiter brings back your order.

Coincidentally, the Chef is the only one who really cares about what method you're using. So when you tell your Waiter to
"GET" something, and the Chef disagrees with your Waiter, it's your Chef who'll win out. Why is this useful? Suppose for a second
your waiter -- drunk on power, maybe -- tells your Chef to GET a API url that really requires a POST. If your Chef knows better,
he'll make the order into a POST. The default Chef is sort of a rookie though, he just does whatever the waiter tells him.
\(You'll probably want to replace him.\)

On the other side of things, there's the Consumer -- he's the dude that your Waiter hands the Chef's delicious indredients to.
He'll nom and crunch them and hopefully transform them into something useable. The default Consumer is the JSONConsumer; Jason,
as I like to refer to him, is also pretty much as dumb as his base Chef counterpart. He'll happily take any response from the
httplib2.Http.request, and try to gnaw his way through to some JSON data and poop it out as a Python data structure.

While this is totally great for simple cases, in more complex situations like dealing with Twitter, it might be a good idea to
give him an idea of what response codes are not desirable -- being able to puke on a 404, or what have you -- or what an error
looks like in that API's data structure, so he can more accurately bubble up errors when you're using your Waiter.

So Why Waiter?
==============

Okay, okay, I know it's not terribly pythonic of me to do what I'm doing here. Overloading operators! Mathematical ones! Purists
are lining the streets, readying themselves with tar and feathers for my imminent march among them. 

So before I get tarred and feathered; let me make some disclaimers. If overloading getattr seems dirty to you, use Waiter. If you don't mind
DSL's -- if you feel like a langauge is a tool, and that tools shouldn't dictate their own use quite so strictly -- use Waiter.
If being Pythonic is more important to you, use Dolt. In short, use what's comfortable for you. I say this, because I care. <3

Keep in mind that one of the main goals for Waiter is to keep things 100% tested; so even while you're using a DSL, you can rest
assured that tests are available for you to run in those dark hours, when using a DSL calls up those darker appetites, and you
feel like you don't know yourself anymore -- like you could even \(gasp!\) start to like DSLs. Let these tests be a salve for your weary soul. 


REQUIREMENTS
============
- python >= 2.5
- httplib2
- urllib
- simplejson
- mox \(for testing\)
