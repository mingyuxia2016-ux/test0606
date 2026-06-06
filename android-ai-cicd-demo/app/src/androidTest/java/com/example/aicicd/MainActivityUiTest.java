package com.example.aicicd;

import androidx.test.ext.junit.rules.ActivityScenarioRule;
import androidx.test.ext.junit.runners.AndroidJUnit4;

import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;

@RunWith(AndroidJUnit4.class)
public class MainActivityUiTest {
    @Rule
    public ActivityScenarioRule<MainActivity> activityRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Test
    public void mainScreenShowsTitle() {
        onView(allOf(
                withId(R.id.title_text),
                withText("Android AI CI/CD Demo")
        )).check(matches(isDisplayed()));
    }

    @Test
    public void mainScreenShowsSubtitle() {
        onView(allOf(
                withId(R.id.subtitle_text),
                withText("Push code to build APK, run tests, and show reports in GitHub Actions.")
        )).check(matches(isDisplayed()));
    }
}
