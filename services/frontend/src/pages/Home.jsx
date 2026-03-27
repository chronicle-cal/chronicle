import React from "react";
import { Link, useLocation } from "react-router-dom";
import {
  Bell,
  Calendar,
  CheckCircle,
  Clock,
  Link2,
  Repeat,
  Settings,
  Sliders,
  Target,
  User,
} from "react-feather";
import { useAuth } from "../context/AuthContext.jsx";

export default function Home() {
  const { isAuthenticated } = useAuth();
  const location = useLocation();
  const from = location.state?.from;
  const features = [
    {
      icon: Repeat,
      title: "Calendar sync",
      description: "Keep calendars aligned automatically.",
    },
    {
      icon: CheckCircle,
      title: "Schedule tasks",
      description:
        "Add your to-dos and time blocks will fly into your calendar.",
    },
    {
      icon: CheckCircle,
      title: "Built for real routines",
      description:
        "Make quick adjustments and keep your week organized as plans change.",
    },
  ];
  const steps = [
    {
      icon: User,
      title: "Create your first profile",
      description:
        "Sign up and create a profile for any area of your life you want to manage.",
    },
    {
      icon: Link2,
      title: "Connect your calendars",
      description:
        "Link your main calendar and select which ones to pull events from and push your schedule to.",
    },
    {
      icon: Calendar,
      title: "Stay up to date",
      description:
        "Chronicle keeps things updated so your schedule stays trustworthy.",
    },
  ];
  const futureFeatures = [
    {
      icon: Bell,
      title: "Smarter reminders",
      description:
        "Configurable nudges for important events and planning windows.",
    },
    {
      icon: Sliders,
      title: "Advanced sync controls",
      description:
        "More rule options for teams, recurring events, and edge cases.",
    },
    {
      icon: Clock,
      title: "Time insights",
      description:
        "A clearer view of schedule balance so you can plan ahead with less effort.",
    },
  ];

  return (
    <div className="hero">
      <section className="home-landing">
        <p className="home-eyebrow">Calendar sync and planning</p>
        <h1 className="home-claim">You're schedule without merge conflicts.</h1>
        <p className="subtle home-intro">
          No AI crap – just clever scheduling algorithms for your calendar.
        </p>
        <div className="actions home-actions">
          {isAuthenticated ? (
            <div className="home-action-wrapper">
              <p className="subtle home-intro">
                You're logged in, so lets head to your
              </p>
              <Link className="btn btn-primary" to="/dashboard">
                Dashboard
              </Link>
            </div>
          ) : (
            <>
              <Link
                className="btn btn-primary"
                to="/register"
                state={from ? { from } : null}
              >
                Get started
              </Link>
              <Link className="btn" to="/login" state={from ? { from } : null}>
                Login
              </Link>
            </>
          )}
        </div>
      </section>

      <section
        className="home-landing home-secondary"
        aria-label="How it works"
      >
        <h2 className="home-section-title">Why Chronicle?</h2>
        <p className="subtle home-section-intro">
          A smart friend for your calendar that helps you stay on top of your
          schedule.
        </p>
        <ol className="home-steps">
          {features.map((feature) => (
            <li className="home-step-item" key={feature.title}>
              <div className="home-item-head">
                <feature.icon className="home-item-icon" size={17} />
                <h3>{feature.title}</h3>
              </div>
              <p className="subtle">{feature.description}</p>
            </li>
          ))}
        </ol>
      </section>

      <section
        className="home-landing home-secondary"
        aria-label="How it works"
      >
        <h2 className="home-section-title">How it works</h2>
        <p className="subtle home-section-intro">
          A straightforward setup that helps you move from disconnected
          calendars to a reliable weekly plan.
        </p>
        <ol className="home-steps">
          {steps.map((step) => (
            <li className="home-step-item" key={step.title}>
              <div className="home-item-head">
                <step.icon className="home-item-icon" size={17} />
                <h3>{step.title}</h3>
              </div>
              <p className="subtle">{step.description}</p>
            </li>
          ))}
        </ol>
      </section>

      <section className="home-landing home-secondary" aria-label="Coming Soon">
        <h2 className="home-section-title">Coming Soon</h2>
        <p className="subtle home-section-intro">
          Planned improvements we’re preparing next.
        </p>
        <ol className="home-steps">
          {futureFeatures.map((feature) => (
            <li className="home-step-item" key={feature.title}>
              <div className="home-item-head">
                <feature.icon className="home-item-icon" size={17} />
                <h3>{feature.title}</h3>
              </div>
              <p className="subtle">{feature.description}</p>
            </li>
          ))}
        </ol>
      </section>
    </div>
  );
}
