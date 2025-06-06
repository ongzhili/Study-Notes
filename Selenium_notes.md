## Loadable Component:

Just a generic class that streamlines the page loading process. (Standardized get() + debug through asserts)
get() -> runs load() then checks isLoaded()

```
Class xxxx extends LoadableComponent<xxxx> {
	@Override
	protected void load() {
		...
	}

	@Override
	protected void isLoaded() throws Error {
		...
	}

	<rest of code here>
}
```

Where xxxx is a Page Object.
Note that isLoaded returns void. Uses assertions for checks.

Allows you to do things like xxxx page = new xxxx(driver).get();


## Bot Pattern

Using `By` in Selenium's documentation.

```
public void click(By locator) {
	driver.findElement(locator).click();
}
```

Abstracts action over raw Selenium API.

# Test Automation

1. Ask yourself if you need a browser to test it. Some functions can be tested through more lightweight test approaches,
like unit tests

By only using the web browser when you have no alternative, you reduce the flake in tests

Manual Testing is recommended if you expect the UI to change considerably in the future.

* Flaky tests in software refer to tests with inconsistent results, even if the component itself has no issue.

2. Abstract out the raw actions (e.g button pressing), so that a test is more readable (ymmv)

The test case should be understandable from a plain view, and the inner functions abstracted out. Makes it easier to modify if the website UI changes
and it is more modular as well 

3. Avoid interaction with the website as much as possible.

e.g We can create different user types in our code with their respectiev credentials. This way, we avoid having to
create a new account every time we want to run a test. <-- Reduce interactions = less flaky


# Types of Testing

## Functional Testing : Building the product **right**

Feature or system functions properly without issue.

## Acceptance Testing : Building the **right** product

Feature or system matches specification

Is a subset of Functional Testing

## Integration testing

Ensure individual modules work together as expected / function properly together

## System Testing

Full e2e testing
- Navigate through all the features of the software and test if the end feature works
- Does not encompass data flow and / or functional testing.

## Performance Testing

- Generally done by executing Selenium tests simulating different users hitting the same function on the web app
- Other tools used to retrieve metrics (e.g JMeter)
	- Metrics include throughput, latency, data loss, component loading times, etc
- Can be classified under 2 broad categories

### Load Testing

Test performance across load levels (e.g 100 users at once)

### Stress testing

Test performance under stress (or above maximum supported load) (e.g holiday sale periods)

## Regression Testing

Usually done after a change / fix / feature add

Ensures that existing functionality isnt broken from a new change.

# Testing in development

## Test Driven Development (TDD)

Development methodology

- Each cycle starts with a set of unit tests
	- Should fail at the start
	- Goal is to pass all of them at the end of the cycle
- Benefit is that potential defects are fixed early


## Behavior-driven development (BDD)

Extension of TDD
- Adds specifications that should fail
- Goal is to pass these + TDD


# Encouraged Testing Practices

## Page Object Model

Essentially 1 Class = 1 Page.

- Tests use class methods in this class to interact with the UI.
	- Page objects themselves do not have any assertions.
		- All asserts / verifications to be in teh tests themselves
		- Except 1, possibly to verify the page (and critical elements on it) are loaded correctly
			- Done when instantiating the page object (a.k.a constructor).
	- You only need to change the logic within the classes
		- All changes to support this UI are located in this class
	- Tests do not need to change
		- Enhances test maintenance
		- Reduce code duplication

Overall results in:
- Clean separation between test code and page code
- Single repository for everything the page offers.

### Page Component Objects

Essentially each object can represent a section of the page instead

Can be included in page objects themselves

Provide similar abstractions.


## Domain Specific Language

Essentially can be summed up to: Design your Page Object / Component classes s.t. the methods 
1. Describe the user action
2. Abstract out the raw Selenium API

## Generating Application State

Pre-load or prepare data without using Selenium (e.g using API to set cookie, instead of logging in via Selenium actions)

## Mock external services

As much as possible, do not depend on external services. You can use fake data / mock a service.

## Avoid Sharing State + Test independency

Each test case should not be reliant on other tests to complete
- Write each test as its own unit.

Each test case should be isolated from one another.
- Do not share test data
- Clean up stale data that might be picked up after a test (e.g invalid orders)
- Create a new WebDriver instance per test

# Discouraged Testing

## CAPTCHAS

Explicitly designed to prevent automation
- Disable CAPTCHAs in test
- Add a hook for tests to bypass CAPTCHAs

## 2FA

Avoid automating 2FA.
- Disable 2FA in test env
- Special token to bypass 2FA
