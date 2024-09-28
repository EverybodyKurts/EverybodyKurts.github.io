---
layout: post
title:  Swift bindings with explicit getters and setters
date:   2020-02-28 12:00:00 -0500
tags: [swift, swiftui]
---

## Introduction

Apple's [SwiftUI tutorials](https://developer.apple.com/tutorials/swiftui/tutorials) do a great job of introducing developers to the fundamental concepts of SwiftUI, including the `@Binding` property wrapper. However, the tutorial doesn't demonstrate how to initialize a `Binding` with an explicit getter and setter via [`init(get:set:)`](https://developer.apple.com/documentation/swiftui/binding/3363053-init). Instead, in files like `LandmarkDetail.swift`, it references the `UserData` as a dependency, thereby prohibiting `LandmarkDetail.swift` from being used with any other data source.

This post will demonstrate how to create bindings with explicit getters and setters so views like `LandmarkDetail.swift` can be reused with any data source that provides a `Landmark`.

## A Simple Example

Let's create a simple SwiftUI view that allows a user to edit the first and last names of people in a list:

{% highlight swift %}
struct Person: Identifiable {
    let id = UUID() // enables iterating with ForEach

    var firstName: String
    var lastName: String
}

struct PersonField: View {
    @Binding var person: Person

    var body: some View {
        HStack {
            TextField("First Name", text: $person.firstName).border(Color.black)
            TextField("Last Name", text: $person.lastName).border(Color.black)
        }
    }
}
{% endhighlight %}

Simple stuff. `PersonField` binds a person's first name and last name to a `TextField` value. When using the view (i.e. composing the `PersonField` view in other views such as `PeopleList`), we'll be iterating through a list of people and creating a `Binding` with a getter and setter for each person.

The following below is our people list:

{% highlight swift %}
struct PeopleList: View {
    @State var people: [Person]

    func personIndex(_ person: Person) -> Int {
        people.firstIndex(where: { $0.id == person.id })!
    }

    var body: some View {
        VStack {
            List {
                ForEach(people) { person in
                    PersonField(person:
                        Binding(
                            get: { person },
                            set: { updatedPerson in
                                self.people[self.personIndex(updatedPerson)] = updatedPerson
                        })
                    )
                }
            }

            ForEach(people) { person in
                Text("\(person.firstName) \(person.lastName)")
            }
        }
    }
}
{% endhighlight %}

This view displays:

1. a row of text fields that allows the user to edit each person's first and last name
2. a collection of `Text` views that display a person's first and last name

The most interesting part of this view is the `Binding` being created for each person as the view iterates through the list of people. We're actually creating a `Binding<Person>` instance for each person, although Swift infers the type of binding from the getter's return value. The binding's `set` closure finds the index of the person, uses array subscript notation to retrieve the correct person, and then assigns the element to be the updated person. The `get` closure simply returns a `Person` instance.

## Updating the Landmark Detail view

Let's update the `LandmarkDetail.swift` view from Apple's tutorials so that it only binds a `Landmark` and doesn't have any explicit dependencies on a list of landmarks.
