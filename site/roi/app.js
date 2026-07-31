const { useState, useEffect, useMemo } = React;

// ---------- small input field ----------
function Field({ label, hint, value, onChange, prefix, suffix, step = 1, min = 0, max }) {
  return (
    <div className="field">
      <label>{label}{hint && <span className="hint">{hint}</span>}</label>
      <div className="input-box">
        {prefix && <span className="affix">{prefix}</span>}
        <input
          type="number" value={value} step={step} min={min} max={max}
          onChange={(e) => {
            const v = e.target.value === '' ? '' : parseFloat(e.target.value);
            onChange(Number.isNaN(v) ? 0 : (v === '' ? 0 : v));
          }}
        />
        {suffix && <span className="affix">{suffix}</span>}
      </div>
    </div>
  );
}

function Group({ title, dot, open, children }) {
  return (
    <details className="group" open={open}>
      <summary>
        {dot && <span className="dot" style={{ background: dot }}></span>}
        {title}
        <span className="chev">▶</span>
      </summary>
      <div className="group-body">{children}</div>
    </details>
  );
}

// ---------- stacked bar ----------
function StackBar({ label, total, totalLabel, segments }) {
  return (
    <div className="bar-block">
      <div className="bar-label"><span>{label}</span><span className="mono">{totalLabel}</span></div>
      <div className="bar">
        {segments.map((s, k) => (
          <span key={k} title={`${s.name}: ${s.value}`} style={{ width: (s.value / total * 100) + '%', background: s.color }}></span>
        ))}
      </div>
      <div className="bar-legend">
        {segments.map((s, k) => (
          <span className="lg" key={k}><span className="sw" style={{ background: s.color }}></span>{s.name} · {s.value}</span>
        ))}
      </div>
    </div>
  );
}

const HUMAN = '#FF2B2B';
const HUMAN_SOFT = '#FF8A80';
const HUMAN_SOFT2 = '#FFC2BB';
const AI = '#000000';
const LIME = '#CCFF00';
const NEUTRAL = '#E7E8EA';
const GREEN = '#16A34A';
const RED_PALE = '#FFD9D4';

// ---------- branded PDF export modal ----------
function ExportModal({ open, brand, setBrand, onClose, onExport, L }) {
  const fileRef = React.useRef(null);
  const [drag, setDrag] = useState(false);
  if (!open) return null;
  const readFile = (file) => {
    if (!file || !file.type.startsWith('image/')) return;
    const fr = new FileReader();
    fr.onload = () => setBrand((b) => ({ ...b, logoDataUrl: fr.result }));
    fr.readAsDataURL(file);
  };
  return (
    <div className="modal-overlay" onMouseDown={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="modal" role="dialog" aria-modal="true">
        <div className="modal-head">
          <h3>{L.exportTitle}</h3>
          <p>{L.exportDesc}</p>
        </div>
        <div className="modal-body">
          <div className="modal-field">
            <label>{L.exportCompany}</label>
            <input type="text" value={brand.companyName} placeholder={L.exportCompanyPh}
              onChange={(e) => setBrand((b) => ({ ...b, companyName: e.target.value }))} />
          </div>
          <div className="modal-field">
            <label>{L.exportLogo}</label>
            <div className={'logo-drop' + (drag ? ' drag' : '') + (brand.logoDataUrl ? ' has' : '')}
              onClick={() => fileRef.current && fileRef.current.click()}
              onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
              onDragLeave={() => setDrag(false)}
              onDrop={(e) => { e.preventDefault(); setDrag(false); readFile(e.dataTransfer.files[0]); }}>
              {brand.logoDataUrl ? (
                <div className="logo-preview">
                  <img src={brand.logoDataUrl} alt="logo" />
                  <button className="logo-remove" onClick={(e) => { e.stopPropagation(); setBrand((b) => ({ ...b, logoDataUrl: '' })); }}>{L.exportRemove}</button>
                </div>
              ) : (
                <div className="logo-empty"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M12 4v11"></path><path d="M7 11l5 5 5-5"></path><path d="M4 20h16"></path></svg><span>{L.exportLogoHint}</span></div>
              )}
            </div>
            <input ref={fileRef} type="file" accept="image/*" style={{ display: 'none' }}
              onChange={(e) => readFile(e.target.files[0])} />
          </div>
        </div>
        <div className="modal-foot">
          <button className="btn-ghost" onClick={onClose}>{L.exportCancel}</button>
          <button className="btn-primary" onClick={onExport}><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 3v12"></path><path d="M7 11l5 5 5-5"></path><path d="M4 20h16"></path></svg>{L.exportGo}</button>
        </div>
      </div>
    </div>
  );
}

function App() {
  const [lang, setLang] = useState(() => localStorage.getItem('sabato_lang') || 'en');
  useEffect(() => { localStorage.setItem('sabato_lang', lang); document.documentElement.lang = lang; }, [lang]);

  const [inp, setInp] = useState(() => {
    try { const s = JSON.parse(localStorage.getItem('sabato_calc')); if (s) return { ...DEFAULTS, ...s }; } catch (e) {}
    return { ...DEFAULTS };
  });
  useEffect(() => { localStorage.setItem('sabato_calc', JSON.stringify(inp)); }, [inp]);
  const set = (k) => (v) => setInp((p) => ({ ...p, [k]: v }));
  const reset = () => setInp({ ...DEFAULTS });

  const L = STR[lang];
  const fmt = useMemo(() => makeFmt(lang), [lang]);
  const r = useMemo(() => compute(inp), [inp]);

  const [brand, setBrand] = useState(() => {
    try { const s = JSON.parse(localStorage.getItem('sabato_brand')); if (s) return { companyName: '', logoDataUrl: '', ...s }; } catch (e) {}
    return { companyName: '', logoDataUrl: '' };
  });
  useEffect(() => { localStorage.setItem('sabato_brand', JSON.stringify(brand)); }, [brand]);
  const [showExport, setShowExport] = useState(false);
  const doExport = () => { setShowExport(false); setTimeout(() => window.print(), 150); };
  const dateStr = useMemo(() => new Date().toLocaleDateString(lang === 'it' ? 'it-IT' : 'en-GB', { year: 'numeric', month: 'long', day: 'numeric' }), [lang]);

  // unit economics of one minute (sums to humanCPM)
  const paidMinYear = Math.max(r.daysWorked * inp.shift * 60, 1);
  const um = {
    salary: inp.ral / paidMinYear,
    contrib: r.employerAddon / paidMinYear,
    idle: Math.max(r.humanCPM - r.costoAzienda / paidMinYear, 0),
    max: Math.max(r.humanCPM, inp.sabatoCPM, 0.0001),
  };

  return (
    <div className="wrap">
      <header className="masthead">
        <div className="topbar">
          <img className="brand-logo" src="brand/sabato-icon.png" alt="Sabato" />
          <div className="topbar-actions">
            <button className="export-btn" onClick={() => setShowExport(true)}><svg className="export-ic" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 3v12"></path><path d="M7 11l5 5 5-5"></path><path d="M4 20h16"></path></svg>{L.exportPdf}</button>
            <div className="lang-switch" role="group" aria-label="Language">
              <button className={lang === 'en' ? 'active' : ''} onClick={() => setLang('en')}>EN</button>
              <button className={lang === 'it' ? 'active' : ''} onClick={() => setLang('it')}>IT</button>
            </div>
          </div>
        </div>
        <span className="eyebrow">{L.badge}</span>
        <h1 className="title">{L.title}</h1>
        <p className="subtitle">{L.subPre}<em>{L.subEm}</em>{L.subPost}</p>
        <p className="meta">{L.eyebrow}</p>
      </header>

      <div className="grid">
        {/* ============ CONTROLS ============ */}
        <aside className="controls panel">
          <div className="controls-head">
            <h2>{L.assumptions}</h2>
            <button className="reset-btn" onClick={reset}>↺ {L.reset}</button>
          </div>

          <Group title={L.gScenario} open={true}>
            <Field label={L.fNumOperators} value={inp.numOperators} onChange={set('numOperators')} min={1} suffix={L.uPpl} />
            <Field label={L.fCallVolume} hint={L.hCallVolume} value={inp.callVolume} onChange={set('callVolume')} step={50} suffix={L.uCalls} />
            <Field label={L.fCallDuration} value={inp.callDuration} onChange={set('callDuration')} step={0.5} suffix={L.uMin} />
          </Group>

          <Group title={L.gSalary} dot={HUMAN} open={true}>
            <Field label={L.fRal} hint={L.hRal} value={inp.ral} onChange={set('ral')} step={500} prefix="€" />
            <Field label={L.fInps} value={Math.round(inp.inpsRate * 1000) / 10} onChange={(v) => set('inpsRate')(v / 100)} step={0.5} suffix="%" />
            <Field label={L.fTfr} value={Math.round(inp.tfrRate * 10000) / 100} onChange={(v) => set('tfrRate')(v / 100)} step={0.1} suffix="%" />
            <Field label={L.fInail} value={Math.round(inp.inailRate * 10000) / 100} onChange={(v) => set('inailRate')(v / 100)} step={0.1} suffix="%" />
          </Group>

          <Group title={L.gOther} dot={HUMAN}>
            <Field label={L.fRecruit} value={inp.recruitment} onChange={set('recruitment')} step={100} prefix="€" />
            <Field label={L.fTraining} value={inp.trainingCost} onChange={set('trainingCost')} step={100} prefix="€" />
          </Group>

          <Group title={L.gDaysOff} dot={HUMAN}>
            <Field label={L.fWeekends} value={inp.weekends} onChange={set('weekends')} suffix={L.uDays} />
            <Field label={L.fHolidays} value={inp.holidays} onChange={set('holidays')} suffix={L.uDays} />
            <Field label={L.fFerie} value={inp.ferie} onChange={set('ferie')} suffix={L.uDays} />
            <Field label={L.fRol} value={inp.rol} onChange={set('rol')} suffix={L.uDays} />
            <Field label={L.fSick} value={inp.sick} onChange={set('sick')} suffix={L.uDays} />
            <Field label={L.fTrainingDays} value={inp.training} onChange={set('training')} suffix={L.uDays} />
            <Field label={L.fClosures} value={inp.closures} onChange={set('closures')} suffix={L.uDays} />
          </Group>

          <Group title={L.gPhone} dot={HUMAN}>
            <Field label={L.fShift} value={inp.shift} onChange={set('shift')} step={0.5} suffix={L.uH} />
            <Field label={L.fLunch} value={inp.lunch} onChange={set('lunch')} step={0.25} suffix={L.uH} />
            <Field label={L.fCoffee} value={inp.coffee} onChange={set('coffee')} step={0.25} suffix={L.uH} />
            <Field label={L.fEmail} value={inp.email} onChange={set('email')} step={0.25} suffix={L.uH} />
            <Field label={L.fCrm} value={inp.crm} onChange={set('crm')} step={0.25} suffix={L.uH} />
            <Field label={L.fMeetings} value={inp.meetings} onChange={set('meetings')} step={0.25} suffix={L.uH} />
          </Group>

          <Group title={L.gSabato} dot={AI} open={true}>
            <Field label={L.fCpm} value={inp.sabatoCPM} onChange={set('sabatoCPM')} step={0.05} prefix="€" />
            <Field label={L.fPlatformFee} value={inp.sabatoMonthlyFee} onChange={set('sabatoMonthlyFee')} step={50} prefix="€" />
            <Field label={L.fSetup} value={inp.sabatoSetup} onChange={set('sabatoSetup')} step={100} prefix="€" />
          </Group>

          <Group title={L.g247}>
            <Field label={L.fAgents247} hint={L.hAgents247} value={inp.agents247} onChange={set('agents247')} suffix={L.uPpl} />
          </Group>
        </aside>

        {/* ============ RESULTS ============ */}
        <main>
          {/* hero stats */}
          <div className="stat-row">
            <div className="stat accent-human">
              <p className="k">{L.sHumanCpm}</p>
              <div className="v mono">{fmt.cpm(r.humanCPM)}</div>
              <div className="sub">{fmt.eur2(r.humanCostPerCall)} {L.perCall}</div>
            </div>
            <div className="stat accent-ai">
              <p className="k">{L.sSabatoCpm}</p>
              <div className="v mono">{fmt.cpm(inp.sabatoCPM)}</div>
              <div className="sub">{fmt.eur2(r.sabatoCostPerCall)} {L.perCall}</div>
            </div>
            <div className="stat accent-save">
              <p className="k">{L.sCheaper}</p>
              <div className="v mono">{fmt.pct(r.pctCheaper)}</div>
              <div className="sub">−{fmt.cpm(r.cpmSavings)} {L.perMin}</div>
            </div>
            <div className="stat accent-save">
              <p className="k">{L.sSaving}</p>
              <div className="v mono">{fmt.eur(r.annualSavings)}</div>
              <div className="sub">{fmt.eur(r.monthlySavings)} {L.perMonth}</div>
            </div>
          </div>

          {/* unit economics of one minute */}
          <div className="panel unitmin">
            <div className="unitmin-head">
              <h4>{L.umTitle}</h4>
              <span className="note">{L.umNote((r.humanCPM / inp.sabatoCPM).toFixed(1).replace('.', lang === 'it' ? ',' : '.') + '×')}</span>
            </div>
            <div className="um-row">
              <div className="um-label"><span className="um-who">{L.umHuman}</span><span className="um-sub">{L.umHumanSub}</span></div>
              <div className="um-track">
                <div className="um-fill" style={{ width: (r.humanCPM / um.max * 100) + '%' }}>
                  <span style={{ flexGrow: um.salary, background: HUMAN }} title={L.umSalary + ' · ' + fmt.cpm(um.salary)}></span>
                  <span style={{ flexGrow: um.contrib, background: HUMAN_SOFT }} title={L.umContrib + ' · ' + fmt.cpm(um.contrib)}></span>
                  <span style={{ flexGrow: um.idle, background: HUMAN_SOFT2 }} title={L.umIdle + ' · ' + fmt.cpm(um.idle)}></span>
                </div>
              </div>
              <div className="um-total" style={{ color: HUMAN }}>{fmt.cpm(r.humanCPM)}</div>
            </div>
            <div className="um-row">
              <div className="um-label"><span className="um-who">{L.umSabato}</span><span className="um-sub">{L.umSabatoSub}</span></div>
              <div className="um-track">
                <div className="um-fill" style={{ width: (inp.sabatoCPM / um.max * 100) + '%' }}>
                  <span style={{ flexGrow: 1, background: 'var(--ink)' }} title={L.umFlat + ' · ' + fmt.cpm(inp.sabatoCPM)}></span>
                </div>
              </div>
              <div className="um-total">{fmt.cpm(inp.sabatoCPM)}</div>
            </div>
            <div className="um-legend">
              <span className="lg"><span className="sw" style={{ background: HUMAN }}></span>{L.umSalary}</span>
              <span className="lg"><span className="sw" style={{ background: HUMAN_SOFT }}></span>{L.umContrib}</span>
              <span className="lg"><span className="sw" style={{ background: HUMAN_SOFT2 }}></span>{L.umIdle}</span>
              <span className="lg"><span className="sw" style={{ background: 'var(--ink)' }}></span>{L.umSabato}</span>
            </div>
          </div>

          {/* comparison */}
          <section className="section">
            <div className="section-head">
              <h3>{L.cmpTitle}</h3>
              <span className="note">{L.cmpNote(fmt.num(inp.callVolume), inp.callDuration, fmt.num(r.totalMinMonth))}</span>
            </div>
            <div className="panel cmp-panel">
              <div className="cmp">
                <div className="cmp-col human">
                  <div className="cmp-tag human"><span className="dot" style={{ background: HUMAN }}></span>{L.humanCol}</div>
                  <div className="li"><span className="lbl">{L.liSalary}</span><span className="val">{fmt.eur(r.costoAzienda)}</span></div>
                  <div className="li"><span className="lbl">{L.liRecruit}</span><span className="val">{fmt.eur(inp.recruitment)}</span></div>
                  <div className="li"><span className="lbl">{L.liTraining}</span><span className="val">{fmt.eur(inp.trainingCost)}</span></div>
                  <div className="li"><span className="lbl">{L.liTurnover}</span><span className="val">{fmt.eur(r.turnover)}</span></div>
                  <div className="li muted"><span className="lbl">{L.liPlatform}</span><span className="val">{fmt.eur(0)}</span></div>
                  <div className="li total human"><span className="lbl">{L.totalYear}</span><span className="val">{fmt.eur(r.humanAnnual)}</span></div>
                  <div className="li"><span className="permo">{L.permo(fmt.eur(r.humanMonthly))}</span></div>
                </div>
                <div className="cmp-col ai">
                  <div className="cmp-tag ai"><span className="dot" style={{ background: LIME }}></span>{L.sabatoCol}</div>
                  <div className="li"><span className="lbl">{L.liSetup}</span><span className="val">{fmt.eur(inp.sabatoSetup)}</span></div>
                  <div className="li"><span className="lbl">{L.liPlatformFee}</span><span className="val">{fmt.eur(r.sabatoPlatformAnnual)}</span></div>
                  <div className="li"><span className="lbl">{L.liUsage(fmt.num(r.totalMinMonth * 12), fmt.cpm(inp.sabatoCPM))}</span><span className="val">{fmt.eur(r.sabatoUsage)}</span></div>
                  <div className="li muted"><span className="lbl">{L.liEmployerNone}</span><span className="val">{fmt.eur(0)}</span></div>
                  <div className="li muted"><span className="lbl">&nbsp;</span><span className="val">&nbsp;</span></div>
                  <div className="li total ai"><span className="lbl">{L.totalYear}</span><span className="val">{fmt.eur(r.sabatoAnnual)}</span></div>
                  <div className="li"><span className="permo">{L.permo(fmt.eur(r.sabatoMonthly))}</span></div>
                </div>
              </div>
              <div className="savings-band">
                <span className="lead">{L.bandLead}</span>
                <span className="pill">{L.bandPill(fmt.pct(r.savingsPct))}</span>
                <span className="big">{L.bandBig(fmt.eur(r.annualSavings))}</span>
              </div>
            </div>
          </section>

          {/* replace your team */}
          <section className="section">
            <div className="section-head">
              <h3>{L.teamTitle}</h3>
              <span className="note">{L.teamNote(inp.numOperators, fmt.num(r.fleetCallsMonth))}</span>
            </div>
            <div className="panel team">
              <div className="team-viz">
                <div className="op-stack">
                  {Array.from({ length: Math.min(inp.numOperators, 24) }).map((_, k) => (<span className="op-glyph" key={k}></span>))}
                  {inp.numOperators > 24 && <span className="op-more">+{inp.numOperators - 24}</span>}
                </div>
                <span className="team-arrow">→</span>
                <div className="ai-glyph"></div>
              </div>
              <div className="s247-grid">
                <div className="s247-cell">
                  <div className="lab">{L.teamYourTeam(inp.numOperators)}</div>
                  <div className="big mono" style={{ color: HUMAN }}>{fmt.eur(r.fleetHumanAnnual)}<span style={{ fontSize: 13, color: 'var(--ink-3)', fontWeight: 400 }}> {L.perYr}</span></div>
                  <div className="small">{fmt.eur(r.fleetHumanMonthly)} {L.perMonth}</div>
                </div>
                <div className="s247-cell">
                  <div className="lab">{L.teamSabato}</div>
                  <div className="big mono" style={{ color: AI }}>{fmt.eur(r.fleetSabatoAnnual)}<span style={{ fontSize: 13, color: 'var(--ink-3)', fontWeight: 400 }}> {L.perYr}</span></div>
                  <div className="small">{fmt.eur(r.fleetSabatoMonthly)} {L.perMonth}</div>
                </div>
                <div className="s247-cell save">
                  <div className="lab">{L.teamSave}</div>
                  <div className="big mono">{fmt.eur(r.fleetSavings)}<span style={{ fontSize: 13, color: 'rgba(204,255,0,.7)', fontWeight: 500 }}> {L.perYr}</span></div>
                  <div className="small">{L.s247Cheaper(fmt.pct(r.fleetSavingsPct))}</div>
                </div>
              </div>
            </div>
          </section>

          {/* buildup */}
          <section className="section">
            <div className="section-head">
              <h3>{L.buildTitle(fmt.cpm(r.humanCPM))}</h3>
              <span className="note">{L.buildNote(fmt.num(inp.ral), fmt.cpm(r.humanCPM))}</span>
            </div>
            <div className="panel buildup">
              <div className="step"><span className="op">RAL</span><span className="desc">{L.stepRal}</span><span className="amt">{fmt.eur(inp.ral)}</span></div>
              <div className="step"><span className="op">+</span><span className="desc">{L.stepEmp} <b>{L.empAdd(fmt.pct(r.employerPct))}</b></span><span className="amt">{fmt.eur(r.employerAddon)}</span></div>
              <div className="step"><span className="op">=</span><span className="desc"><b>{L.stepCosto}</b></span><span className="amt">{fmt.eur(r.costoAzienda)}</span></div>
              <div className="step"><span className="op">÷</span><span className="desc">{L.stepDiv}</span><span className="amt">{fmt.num(r.productiveMinYear)}</span></div>
              <div className="step result"><span className="op">=</span><span className="desc">{L.stepResult}</span><span className="amt mono">{fmt.cpm(r.humanCPM)}</span></div>

              <div className="two-col" style={{ padding: '18px 0 2px' }}>
                <StackBar
                  label={L.barDays}
                  total={365}
                  totalLabel={L.barDaysTotal(r.daysWorked, fmt.pct(r.daysWorked / 365))}
                  segments={[
                    { name: L.segWorked, value: r.daysWorked, color: GREEN },
                    { name: L.segWeekends, value: inp.weekends, color: NEUTRAL },
                    { name: L.segHolidays, value: inp.holidays + inp.ferie + inp.rol, color: HUMAN_SOFT2 },
                    { name: L.segSick, value: inp.sick + inp.training + inp.closures, color: HUMAN_SOFT },
                  ]}
                />
                <StackBar
                  label={L.barHours}
                  total={inp.shift}
                  totalLabel={L.barHoursTotal(fmt.hours(r.phoneHours), fmt.pct(r.utilization))}
                  segments={[
                    { name: L.segPhone, value: r.phoneHours, color: GREEN },
                    { name: L.segCrm, value: inp.crm, color: NEUTRAL },
                    { name: L.segEmail, value: inp.email, color: HUMAN_SOFT2 },
                    { name: L.segLunch, value: inp.lunch, color: HUMAN_SOFT },
                    { name: L.segBreaks, value: inp.coffee + inp.meetings, color: RED_PALE },
                  ]}
                />
              </div>
            </div>
          </section>

          {/* operational comparison */}
          <section className="section">
            <div className="section-head"><h3>{L.opsTitle}</h3></div>
            <div className="panel ops">
              <div className="ops-row">
                <span className="ops-head">{L.opsMetric}</span>
                <span className="ops-head" style={{ color: HUMAN }}>{L.opsHuman}</span>
                <span className="ops-head" style={{ color: AI }}>{L.opsAI}</span>
              </div>
              {L.opsRows(fmt, inp).map((row, k) => (
                <div className="ops-row" key={k}>
                  <span className="ops-k">{row[0]}</span>
                  <span className="ops-cell h">{row[1]}</span>
                  <span className="ops-cell a">{row[2]}</span>
                </div>
              ))}
            </div>
          </section>

          {/* 24/7 */}
          <section className="section">
            <div className="section-head">
              <h3>{L.s247Title}</h3>
              <span className="note">{L.s247Note(inp.agents247)}</span>
            </div>
            <div className="panel scenario247">
              <div className="s247-grid">
                <div className="s247-cell">
                  <div className="lab">{L.s247Human(inp.agents247)}</div>
                  <div className="big mono" style={{ color: HUMAN }}>{fmt.eur(r.human247Annual)}<span style={{ fontSize: 13, color: 'var(--ink-3)', fontWeight: 400 }}> {L.perYr}</span></div>
                  <div className="small">{fmt.eur(r.human247Monthly)} {L.perMonth}</div>
                </div>
                <div className="s247-cell">
                  <div className="lab">{L.s247Sabato}</div>
                  <div className="big mono" style={{ color: AI }}>{fmt.eur(r.sabato247Annual)}<span style={{ fontSize: 13, color: 'var(--ink-3)', fontWeight: 400 }}> {L.perYr}</span></div>
                  <div className="small">{fmt.eur(r.sabato247Monthly)} {L.perMonth}</div>
                </div>
                <div className="s247-cell save">
                  <div className="lab">{L.s247Save}</div>
                  <div className="big mono">{fmt.eur(r.savings247)}<span style={{ fontSize: 13, color: 'rgba(204,255,0,.7)', fontWeight: 500 }}> {L.perYr}</span></div>
                  <div className="small">{L.s247Cheaper(fmt.pct(r.savings247 / r.human247Annual))}</div>
                </div>
              </div>
            </div>
          </section>

          <p className="footnote">{L.footnote}</p>
        </main>
      </div>

      <ReportSheet brand={brand} inp={inp} r={r} fmt={fmt} L={L} dateStr={dateStr} />

      <ExportModal open={showExport} brand={brand} setBrand={setBrand}
        onClose={() => setShowExport(false)} onExport={doExport} L={L} />
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
