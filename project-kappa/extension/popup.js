// Load last audit result from Chrome storage and display it
chrome.storage.local.get(['lastAudit'], function(result) {
  if (!result.lastAudit) return;
  
  const audit = result.lastAudit;
  const statusBox = document.getElementById('statusBox');
  const scoresPanel = document.getElementById('scoresPanel');
  const flaggedPanel = document.getElementById('flaggedPanel');
  const alternativesPanel = document.getElementById('alternativesPanel');

  // Set traffic light
  statusBox.className = 'status-box ' + audit.verdict;
  const labels = {
    green: '✅ Contextually Relevant',
    orange: '⚠️ Partial Displacement Detected',
    red: '🚨 High Contextual Displacement'
  };
  document.querySelector('.status-label').textContent = labels[audit.verdict];

  // Show scores
  scoresPanel.style.display = 'block';
  document.getElementById('cdiScore').textContent = audit.cdi_score.toFixed(2);
  document.getElementById('rasScore').textContent = audit.ras_score.toFixed(2);
  document.getElementById('atdScore').textContent = audit.atd_score.toFixed(2);
  document.getElementById('llsScore').textContent = audit.lls_score.toFixed(2);

  // Show flagged terms
  if (audit.flagged_terms && audit.flagged_terms.length > 0) {
    flaggedPanel.style.display = 'block';
    const list = document.getElementById('flaggedList');
    audit.flagged_terms.forEach(term => {
      const tag = document.createElement('span');
      tag.className = 'flagged-tag';
      tag.textContent = term;
      list.appendChild(tag);
    });
  }

  // Show sovereign alternatives
  if (audit.sovereign_alternatives && audit.sovereign_alternatives.length > 0) {
    alternativesPanel.style.display = 'block';
    const altList = document.getElementById('altList');
    audit.sovereign_alternatives.forEach(alt => {
      const card = document.createElement('div');
      card.className = 'alt-card';
      card.innerHTML = `
        <div class="alt-name">${alt.name}</div>
        <div class="alt-country">${alt.country}</div>
        <div class="alt-desc">${alt.description}</div>
        <a class="alt-link" href="${alt.url}" target="_blank">→ Visit</a>
      `;
      altList.appendChild(card);
    });
  }
});