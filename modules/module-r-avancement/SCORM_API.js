/**
 * SCORM 2004 API �?" Wrapper partagé (Initialize/Terminate, CMI 2004)
 * L'esprit d'innover �?" Projet modulaire SCORM
 * Utilisation : <script src="SCORM_API.js"></script> puis ScormAPI.* ou API.LMS*.
 * Compatible LMS SCORM 2004 (4th Edition). Aliases LMS* pour usage identique au 1.2.
 */

(function (global) {
  'use strict';

  function searchWin(w) {
    while (w) {
      for (var i = 0; i < 8; i++) {
        var name = i === 0 ? 'API' : 'API_' + i;
        if (w[name]) return w[name];
      }
      if (w === w.parent) break;
      w = w.parent;
    }
    return null;
  }

  var findAPI = function (win) {
    if (!win) return null;
    var api = searchWin(win);
    if (api) return api;
    if (win.opener) api = searchWin(win.opener);
    return api || null;
  };

  var api = findAPI(typeof window !== 'undefined' ? window : global);

  function callGetValue(key) {
    if (!api) return '';
    try {
      if (typeof api.GetValue === 'function') return api.GetValue(key) || '';
      if (typeof api.LMSGetValue === 'function') return api.LMSGetValue(key) || '';
    } catch (e) {}
    return '';
  }

  function callSetValue(key, value) {
    if (!api) return false;
    try {
      if (typeof api.SetValue === 'function') return api.SetValue(key, String(value)) !== 'false';
      if (typeof api.LMSSetValue === 'function') return api.LMSSetValue(key, String(value)) !== 'false';
    } catch (e) {}
    return false;
  }

  function callCommit() {
    if (!api) return false;
    try {
      if (typeof api.Commit === 'function') return api.Commit('');
      if (typeof api.LMSCommit === 'function') return api.LMSCommit('');
    } catch (e) {}
    return false;
  }

  var scorm = {
    isAvailable: function () { return api != null; },
    getValue: function (key) { return callGetValue(key); },
    setValue: function (key, value) { return callSetValue(key, value); },
    getSuspendData: function () { return callGetValue('cmi.suspend_data'); },
    setSuspendData: function (data) { return callSetValue('cmi.suspend_data', data); },
    commit: function () { return callCommit(); },
    /** SCORM 2004 : cmi.completion_status ("completed" | "incomplete" | "not attempted" | "unknown") */
    setLessonStatus: function (status) {
      if (!api) return false;
      return callSetValue('cmi.completion_status', status);
    },
    /** SCORM 2004 : cmi.score.scaled (0..1) + raw/min/max pour compatibilité */
    setScore: function (raw, min, max) {
      if (!api) return false;
      var mn = min != null ? Number(min) : 0;
      var mx = max != null ? Number(max) : 100;
      var r = Number(raw);
      var scaled = (mx - mn) !== 0 ? (r - mn) / (mx - mn) : 0;
      if (scaled < 0) scaled = 0;
      if (scaled > 1) scaled = 1;
      callSetValue('cmi.score.scaled', scaled);
      callSetValue('cmi.score.raw', r);
      callSetValue('cmi.score.min', mn);
      callSetValue('cmi.score.max', mx);
      return true;
    },
    /* Aliases pour onload/onbeforeunload : 2004 (Initialize/Terminate) ou 1.2 (LMSInitialize/LMSFinish) */
    LMSInitialize: function () {
      if (!api) return 'false';
      try {
        if (typeof api.Initialize === 'function') return api.Initialize('') ? 'true' : 'false';
        if (typeof api.LMSInitialize === 'function') return api.LMSInitialize('');
      } catch (e) {}
      return 'true';
    },
    LMSCommit: function () { return this.commit() ? 'true' : 'false'; },
    LMSFinish: function () {
      if (!api) return;
      try {
        if (typeof api.Terminate === 'function') api.Terminate('');
        else if (typeof api.LMSFinish === 'function') api.LMSFinish('');
      } catch (e) {}
    },
    LMSGetValue: function (key) { return this.getValue(key); },
    LMSSetValue: function (key, value) { return this.setValue(key, value); }
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = scorm;
  } else {
    global.ScormAPI = scorm;
    global.API = scorm;
  }
})(typeof window !== 'undefined' ? window : this);
