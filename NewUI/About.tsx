import React from 'react';
import { Info, Heart, ExternalLink, Github, Mail } from 'lucide-react';

export default function About() {
  return (
    <div className="px-5 pt-12 pb-4">
      <div className="flex items-center gap-2 mb-6">
        <Info className="w-6 h-6" />
        <h1 className="text-2xl font-bold">About</h1>
      </div>

      {/* App Info */}
      <div className="flex flex-col items-center text-center bg-card rounded-2xl border border-border/50 p-6 mb-5">
        <img src="https://media.base44.com/images/public/69ba840ff9da585908580590/e04cf0bb2_logo2.png" alt="Vocynx" className="h-16 w-auto mb-3" />
        <span className="text-xs font-semibold bg-muted text-muted-foreground px-2.5 py-0.5 rounded-full mt-1">
          Open Source
        </span>
        <p className="text-sm text-muted-foreground mt-3">Version 2.4.0</p>
      </div>

      {/* Description */}
      <div className="bg-card rounded-xl border border-border/50 p-4 mb-5">
        <p className="text-sm leading-relaxed text-muted-foreground">
          Vocynx is a free, open-source voice-to-text app powered by OpenAI Whisper. Transcribe speech in real-time with optional LLM refinement — no subscription, no lock-in.
        </p>
      </div>

      {/* Tech Info */}
      <div className="bg-card rounded-xl border border-border/50 p-4 mb-5">
        <h3 className="text-xs font-semibold text-muted-foreground tracking-wider uppercase mb-3">Technology</h3>
        <div className="space-y-2.5">
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">Speech Engine</span>
            <span className="font-medium">OpenAI Whisper</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">LLM Support</span>
            <span className="font-medium">OpenAI, Groq</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">Framework</span>
            <span className="font-medium">PySide6 / Qt</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">Platform</span>
            <span className="font-medium">Cross-platform</span>
          </div>
        </div>
      </div>

      {/* Links */}
      <div className="bg-card rounded-xl border border-border/50 divide-y divide-border/40 mb-5">
        <button className="w-full flex items-center justify-between px-4 py-3.5 text-sm">
          <div className="flex items-center gap-2.5">
            <Github className="w-4 h-4 text-muted-foreground" />
            <span>Source Code</span>
          </div>
          <ExternalLink className="w-4 h-4 text-muted-foreground" />
        </button>
        <button className="w-full flex items-center justify-between px-4 py-3.5 text-sm">
          <div className="flex items-center gap-2.5">
            <Mail className="w-4 h-4 text-muted-foreground" />
            <span>Contact Support</span>
          </div>
          <ExternalLink className="w-4 h-4 text-muted-foreground" />
        </button>
      </div>

      {/* Footer */}
      <div className="text-center py-4">
        <p className="text-xs text-muted-foreground flex items-center justify-center gap-1">
          Made with <Heart className="w-3 h-3 text-red-400 fill-red-400" /> by the Vocynx contributors
        </p>
        <p className="text-[10px] text-muted-foreground/60 mt-1">© 2026 Vocynx. Open Source.</p>
      </div>
    </div>
  );
}