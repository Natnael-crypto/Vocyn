import React from 'react';
import { Shield, CheckCircle, Crown, Zap } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

const features = [
    { label: 'Unlimited transcriptions', included: true },
    { label: 'All Whisper models (tiny, base, small)', included: true },
    { label: 'LLM refinement (OpenAI, Groq)', included: true },
    { label: 'Real-time translation', included: true },
    { label: 'Custom hotkey support', included: true },
    { label: 'Priority support', included: true },
];

export default function License() {
    return (
        <div className="px-5 pt-12 pb-4">
            <div className="flex items-center gap-2 mb-6">
                <Shield className="w-6 h-6" />
                <h1 className="text-2xl font-bold">License</h1>
            </div>

            {/* Current Plan */}
            <div className="bg-secondary rounded-2xl p-5 mb-5">
                <div className="flex items-center gap-2 mb-2">
                    <Crown className="w-5 h-5 text-yellow-600" />
                    <span className="font-semibold">Vocynx</span>
                    <Badge className="text-[10px] bg-muted text-muted-foreground">Open Source</Badge>
                </div>
                <p className="text-sm text-muted-foreground">
                    Vocynx is free and open source. All features are available to everyone.
                </p>
            </div>

            {/* License Details */}
            <div className="bg-card rounded-xl border border-border/50 p-4 mb-5">
                <h3 className="text-xs font-semibold text-muted-foreground tracking-wider uppercase mb-3">License Details</h3>
                <div className="space-y-2.5">
                    <div className="flex justify-between text-sm">
                        <span className="text-muted-foreground">License Type</span>
                        <span className="font-medium">MIT License</span>
                    </div>
                    <div className="flex justify-between text-sm">
                        <span className="text-muted-foreground">Repository</span>
                        <span className="font-medium">github.com/vocynx</span>
                    </div>
                    <div className="flex justify-between text-sm">
                        <span className="text-muted-foreground">First Release</span>
                        <span className="font-medium">2025</span>
                    </div>
                    <div className="flex justify-between text-sm">
                        <span className="text-muted-foreground">Cost</span>
                        <span className="font-medium">Free forever</span>
                    </div>
                </div>
            </div>

            {/* Features */}
            <div className="bg-card rounded-xl border border-border/50 p-4">
                <h3 className="text-xs font-semibold text-muted-foreground tracking-wider uppercase mb-3">Included Features</h3>
                <div className="space-y-3">
                    {features.map((f, i) => (
                        <div key={i} className="flex items-center gap-2.5">
                            <CheckCircle className="w-4 h-4 text-green-500 shrink-0" />
                            <span className="text-sm">{f.label}</span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Upgrade CTA */}
            <div className="mt-5 bg-card rounded-xl border border-border/50 p-4 flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-secondary flex items-center justify-center shrink-0">
                    <Zap className="w-5 h-5 text-yellow-600" />
                </div>
                <div>
                    <p className="text-sm font-medium">Need more power?</p>
                    <p className="text-xs text-muted-foreground">Explore enterprise plans for team licensing.</p>
                </div>
            </div>
        </div>
    );
}