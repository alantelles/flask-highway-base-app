# Flask Highway Base App

## A post-framework built on top of Flask

This is the base app that will be downloaded by Highway when you do a `highway new [project]` on terminal.

The goal is to provide the basic you need to start an application as well propose a good structure to your Flask apps. It means that as opposite to pure Flask, Highway tend to be highly opinionated.

This application has an embedded login system with roles permission setup. Additionally features decorators so you can restrict the access to views by roles names.

It also features an auditor which exposes a decorator to audit certain views you want.


All this in the box, at a `git clone` from your fingers.

The Flask-Highway CLI is in development and promises to provide a great speed and organization in Flask development.

Flask Highway is assumed highly inspired in Ruby on Rails.

Documentation in course.