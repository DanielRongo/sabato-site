// ============================================================
//  ReportSheet — one-page, board-ready PDF report (print only)
//  Pulls the same live figures the calculator computes.
// ============================================================
function ReportSheet({ brand, inp, r, fmt, L, dateStr }) {
  return (
    <div className="report-sheet">
      <div className="rs-head">
        <div className="rs-co">
          {brand.logoDataUrl && <img src={brand.logoDataUrl} className="rs-logo" alt="" />}
          <div className="rs-co-text">
            <div className="rs-sub">{L.reportPreparedFor}</div>
            <div className="rs-name">{brand.companyName || '—'}</div>
          </div>
        </div>
        <div className="rs-meta">
          <div className="rs-powered">{L.poweredBy}</div>
          <img src="brand/sabato-icon.png" className="rs-sabato" alt="Sabato" />
          <div className="rs-date">{dateStr}</div>
        </div>
      </div>

      <div className="rs-eyebrow">{L.rpBrief} · {L.rpTopic}</div>
      <h2 className="rs-headline">{L.rpHeadline(fmt.eur(r.annualSavings))}</h2>
      <p className="rs-lede">{L.rpLede(fmt.cpm(r.humanCPM), fmt.cpm(inp.sabatoCPM), fmt.pct(r.pctCheaper))}</p>

      <div className="rs-kpis">
        <div className="rs-kpi">
          <div className="rs-kv">{fmt.eur(r.annualSavings)}</div>
          <div className="rs-kl">{L.rpK1}</div>
          <div className="rs-ks">{L.rpK1sub(fmt.pct(r.savingsPct))}</div>
        </div>
        <div className="rs-kpi">
          <div className="rs-kv">{fmt.cpm(r.humanCPM)}<span className="rs-arrow"> → </span>{fmt.cpm(inp.sabatoCPM)}</div>
          <div className="rs-kl">{L.rpK2}</div>
          <div className="rs-ks">{L.rpK2sub}</div>
        </div>
        <div className="rs-kpi">
          <div className="rs-kv">{fmt.eur(r.fleetSavings)}</div>
          <div className="rs-kl">{L.rpK3(inp.numOperators)}</div>
          <div className="rs-ks">{L.rpK3sub(fmt.pct(r.fleetSavingsPct))}</div>
        </div>
        <div className="rs-kpi rs-kpi-dark">
          <div className="rs-kv">{fmt.eur(r.savings247)}</div>
          <div className="rs-kl">{L.rpK4}</div>
          <div className="rs-ks">{L.rpK4sub(inp.agents247)}</div>
        </div>
      </div>

      <div className="rs-cols">
        <div className="rs-col">
          <div className="rs-ct">{L.rpWhyTitle(fmt.cpm(r.humanCPM))}</div>
          <div className="rs-pt"><span className="rs-dot rs-dot-h"></span><div><b>{L.rpWhy1h}</b><span>{L.rpWhy1(fmt.pct(r.employerPct))}</span></div></div>
          <div className="rs-pt"><span className="rs-dot rs-dot-h"></span><div><b>{L.rpWhy2h}</b><span>{L.rpWhy2(fmt.num(r.daysWorked) + ' / 365')}</span></div></div>
          <div className="rs-pt"><span className="rs-dot rs-dot-h"></span><div><b>{L.rpWhy3h}</b><span>{L.rpWhy3(fmt.pct(r.utilization))}</span></div></div>
        </div>
        <div className="rs-col">
          <div className="rs-ct">{L.rpEdgeTitle}</div>
          <div className="rs-pt"><span className="rs-dot rs-dot-a"></span><div><b>{L.rpEdge1h}</b><span>{L.rpEdge1}</span></div></div>
          <div className="rs-pt"><span className="rs-dot rs-dot-a"></span><div><b>{L.rpEdge2h}</b><span>{L.rpEdge2}</span></div></div>
          <div className="rs-pt"><span className="rs-dot rs-dot-a"></span><div><b>{L.rpEdge3h}</b><span>{L.rpEdge3}</span></div></div>
        </div>
      </div>

      <div className="rs-compare">{L.rpCompare(fmt.eur(r.humanAnnual), fmt.eur(r.sabatoAnnual))}</div>

      <div className="rs-foot">
        <span className="rs-foot-note">{L.reportFooter}</span>
        <span className="rs-conf">{L.rpFooterConf}</span>
      </div>
    </div>
  );
}
