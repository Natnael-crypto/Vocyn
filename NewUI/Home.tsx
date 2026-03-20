import React from 'react';
import WelcomeBanner from '../components/home/WelcomeBanner';
import StatsBar from '../components/home/StatsBar';
import ActivityItem from '../components/home/ActivityItem';

const activities = [
    { time: '12:38 PM', text: 'I want to draft an email for holiday seasons' },
    { time: '12:38 PM', text: 'Email is ready. Could you help me check if this sentence is right?' },
    { time: '12:38 PM', text: 'Audio is silence', isAudioNote: true },
    { time: '12:39 PM', text: 'Could you please review this attachment and provide your feedback?' },
    { time: '12:40 PM', text: 'I need assistance in finalizing the presentation for tomorrow\'s meeting.' },
    { time: '12:41 PM', text: 'Let\'s schedule a call to discuss the project updates.' },
];

export default function Home() {
    return (
        <div className="px-5 pt-12 pb-4">
            {/* Header */}
            <div className="flex items-center gap-2 mb-1">
                <img src="https://media.base44.com/images/public/69ba840ff9da585908580590/e04cf0bb2_logo2.png" alt="Vocynx" className="h-7 w-auto" />
            </div>
            <h1 className="text-2xl font-bold mt-4 mb-3">Welcome back 👋</h1>

            {/* Stats */}
            <StatsBar />

            {/* Banner */}
            <div className="mt-4">
                <WelcomeBanner />
            </div>

            {/* Activity */}
            <div className="mt-6">
                <p className="text-xs font-semibold text-muted-foreground tracking-wider uppercase mb-2">Today</p>
                <div className="bg-card rounded-xl border border-border/50 px-4">
                    {activities.map((item, i) => (
                        <ActivityItem key={i} time={item.time} text={item.text} isAudioNote={item.isAudioNote} />
                    ))}
                </div>
            </div>
        </div>
    );
}