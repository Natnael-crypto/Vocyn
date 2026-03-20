import React, { useState, useCallback } from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';
import { Slider } from '@/components/ui/slider';
import { Input } from '@/components/ui/input';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Settings as SettingsIcon, Save } from 'lucide-react';
import { toast } from 'sonner';
import SettingSection from '../components/settings/SettingSection';
import SettingRow from '../components/settings/SettingRow';

const WHISPER_LANGUAGES = [
  { label: 'Auto Detect', code: 'auto' },
  { label: 'English', code: 'en' },
  { label: 'Spanish', code: 'es' },
  { label: 'French', code: 'fr' },
  { label: 'German', code: 'de' },
  { label: 'Chinese', code: 'zh' },
  { label: 'Japanese', code: 'ja' },
  { label: 'Korean', code: 'ko' },
  { label: 'Arabic', code: 'ar' },
  { label: 'Hindi', code: 'hi' },
  { label: 'Portuguese', code: 'pt' },
  { label: 'Russian', code: 'ru' },
  { label: 'Italian', code: 'it' },
];

const LLM_MODELS = {
  None: {},
  OpenAI: {
    'GPT-4': ['gpt-4', 'gpt-4-turbo', 'gpt-4o'],
    'GPT-3.5': ['gpt-3.5-turbo'],
  },
  Groq: {
    'Llama': ['llama-3.1-70b-versatile', 'llama-3.1-8b-instant'],
    'Mixtral': ['mixtral-8x7b-32768'],
  },
};

const HOTKEYS = ['ctrl+alt+space', 'ctrl+shift+space', 'alt+space', 'shift+f12'];
const MICROPHONES = ['Default Microphone', 'Built-in Microphone', 'USB Audio Device', 'Bluetooth Headset'];

const defaultConfig = {
  audioDevice: 'Default Microphone',
  language: 'auto',
  mode: 'transcribe',
  targetLanguage: 'en',
  transcriptionModel: 'base',
  silenceTimeout: 15,
  hotkey: 'ctrl+alt+space',
  runMinimized: false,
  llmProvider: 'None',
  llmCategory: '',
  llmModel: '',
  llmApiKey: '',
};

export default function Settings() {
  const [config, setConfig] = useState(defaultConfig);

  const update = useCallback((key, value) => {
    setConfig(prev => ({ ...prev, [key]: value }));
  }, []);

  const onProviderChange = useCallback((provider) => {
    const categories = Object.keys(LLM_MODELS[provider] || {});
    const firstCat = categories[0] || '';
    const models = LLM_MODELS[provider]?.[firstCat] || [];
    setConfig(prev => ({
      ...prev,
      llmProvider: provider,
      llmCategory: firstCat,
      llmModel: models[0] || '',
    }));
  }, []);

  const onCategoryChange = useCallback((category) => {
    setConfig(prev => {
      const models = LLM_MODELS[prev.llmProvider]?.[category] || [];
      const keepModel = models.includes(prev.llmModel) ? prev.llmModel : models[0] || '';
      return { ...prev, llmCategory: category, llmModel: keepModel };
    });
  }, []);

  const saveSettings = () => {
    toast.success('Settings saved successfully');
  };

  const categories = Object.keys(LLM_MODELS[config.llmProvider] || {});
  const models = LLM_MODELS[config.llmProvider]?.[config.llmCategory] || [];
  const targetLanguages = WHISPER_LANGUAGES.filter(l => l.code !== 'auto');

  return (
    <div className="px-5 pt-12 pb-4">
      <div className="flex items-center gap-2 mb-6">
        <SettingsIcon className="w-6 h-6" />
        <h1 className="text-2xl font-bold">Settings</h1>
      </div>

      {/* Audio Device */}
      <SettingSection title="Audio">
        <SettingRow label="Microphone" description="Select audio input device">
          <Select value={config.audioDevice} onValueChange={v => update('audioDevice', v)}>
            <SelectTrigger className="w-40 h-8 text-xs">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {MICROPHONES.map(mic => (
                <SelectItem key={mic} value={mic} className="text-xs">{mic}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </SettingRow>
      </SettingSection>

      {/* Language */}
      <SettingSection title="Language">
        <SettingRow label="Input Language" description="Whisper language for transcription">
          <Select value={config.language} onValueChange={v => update('language', v)}>
            <SelectTrigger className="w-32 h-8 text-xs">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {WHISPER_LANGUAGES.map(l => (
                <SelectItem key={l.code} value={l.code} className="text-xs">{l.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </SettingRow>
      </SettingSection>

      {/* Transcription Mode */}
      <SettingSection title="Transcription Mode">
        <div className="px-4 py-3.5">
          <RadioGroup value={config.mode} onValueChange={v => update('mode', v)} className="space-y-3">
            <div className="flex items-center gap-2">
              <RadioGroupItem value="transcribe" id="transcribe" />
              <Label htmlFor="transcribe" className="text-sm">Transcribe only</Label>
            </div>
            <div className="flex items-center gap-2">
              <RadioGroupItem value="translate" id="translate" />
              <Label htmlFor="translate" className="text-sm">Translation</Label>
            </div>
          </RadioGroup>
          {config.mode === 'translate' && (
            <div className="mt-3 flex items-center justify-between">
              <span className="text-sm text-muted-foreground">Target Language</span>
              <Select value={config.targetLanguage} onValueChange={v => update('targetLanguage', v)}>
                <SelectTrigger className="w-32 h-8 text-xs">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {targetLanguages.map(l => (
                    <SelectItem key={l.code} value={l.code} className="text-xs">{l.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}
        </div>
      </SettingSection>

      {/* LLM Refinement */}
      <SettingSection title="LLM Refinement">
        <SettingRow label="Provider">
          <Select value={config.llmProvider} onValueChange={onProviderChange}>
            <SelectTrigger className="w-28 h-8 text-xs">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {Object.keys(LLM_MODELS).map(p => (
                <SelectItem key={p} value={p} className="text-xs">{p}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </SettingRow>
        {config.llmProvider !== 'None' && (
          <>
            <SettingRow label="Category">
              <Select value={config.llmCategory} onValueChange={onCategoryChange}>
                <SelectTrigger className="w-28 h-8 text-xs">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {categories.map(c => (
                    <SelectItem key={c} value={c} className="text-xs">{c}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </SettingRow>
            <SettingRow label="Model">
              <Select value={config.llmModel} onValueChange={v => update('llmModel', v)}>
                <SelectTrigger className="w-40 h-8 text-xs">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {models.map(m => (
                    <SelectItem key={m} value={m} className="text-xs">{m}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </SettingRow>
            <SettingRow label="API Key">
              <Input
                type="password"
                value={config.llmApiKey}
                onChange={e => update('llmApiKey', e.target.value)}
                placeholder="Enter key"
                className="w-40 h-8 text-xs"
              />
            </SettingRow>
          </>
        )}
      </SettingSection>

      {/* Transcription Model */}
      <SettingSection title="Transcription Model">
        <SettingRow label="Whisper Model" description="Larger models are more accurate but slower">
          <Select value={config.transcriptionModel} onValueChange={v => update('transcriptionModel', v)}>
            <SelectTrigger className="w-24 h-8 text-xs">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="tiny" className="text-xs">Tiny</SelectItem>
              <SelectItem value="base" className="text-xs">Base</SelectItem>
              <SelectItem value="small" className="text-xs">Small</SelectItem>
            </SelectContent>
          </Select>
        </SettingRow>
      </SettingSection>

      {/* Silence Timeout */}
      <SettingSection title="Silence Timeout">
        <div className="px-4 py-3.5">
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm font-medium">Timeout Duration</span>
            <span className="text-sm font-semibold tabular-nums">{(config.silenceTimeout / 10).toFixed(1)}s</span>
          </div>
          <Slider
            value={[config.silenceTimeout]}
            onValueChange={([v]) => update('silenceTimeout', v)}
            min={8}
            max={25}
            step={1}
            className="w-full"
          />
          <div className="flex justify-between mt-1.5">
            <span className="text-[10px] text-muted-foreground">0.8s</span>
            <span className="text-[10px] text-muted-foreground">2.5s</span>
          </div>
        </div>
      </SettingSection>

      {/* Hotkey */}
      <SettingSection title="Global Hotkey">
        <SettingRow label="Shortcut" description="Toggle transcription">
          <Select value={config.hotkey} onValueChange={v => update('hotkey', v)}>
            <SelectTrigger className="w-36 h-8 text-xs">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {HOTKEYS.map(h => (
                <SelectItem key={h} value={h} className="text-xs">{h}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </SettingRow>
      </SettingSection>

      {/* Run in Tray */}
      <SettingSection title="System">
        <SettingRow label="Run in Tray" description="Minimize to system tray on close">
          <Switch checked={config.runMinimized} onCheckedChange={v => update('runMinimized', v)} />
        </SettingRow>
      </SettingSection>

      {/* Save Button */}
      <Button onClick={saveSettings} className="w-full h-11 rounded-xl font-semibold gap-2 mb-4">
        <Save className="w-4 h-4" />
        Save Settings
      </Button>
    </div>
  );
}