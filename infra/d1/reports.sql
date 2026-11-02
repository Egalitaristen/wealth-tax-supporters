-- Mistake reports sent from the site's /report form. Lives only in Cloudflare D1 (database wts-suggestions, next to
-- the suggestions and feedback tables); never committed to git. Review with: python scripts/suggestions.py reports
-- A report is a lead, not evidence: check it against the source before changing an entry. No names or contact details
-- are required. contact is an optional address the sender chooses to give if they want a reply. ip_hash is a keyed hash
-- of the sender's IP and the day, used only to limit how many a sender can send in a day.

CREATE TABLE IF NOT EXISTS reports (
  id          TEXT PRIMARY KEY,                  -- random UUID
  created_at  TEXT NOT NULL,                     -- ISO 8601, UTC
  kind        TEXT NOT NULL CHECK (kind IN ('wrong', 'removal')),  -- something is wrong | remove or correct an entry about me
  country     TEXT,                              -- the country folder, for example gb
  entry       TEXT,                              -- actor ID (A0123)
  evidence    TEXT,                              -- evidence ID (E00123), when the report is about one source
  page        TEXT,                              -- the site page it was sent from
  message     TEXT NOT NULL,                     -- what is wrong
  source_url  TEXT,                              -- optional: a link that shows it (http or https)
  contact     TEXT,                              -- optional: how to reply
  ip_hash     TEXT NOT NULL,
  status      TEXT NOT NULL DEFAULT 'new'        -- new | done | wontfix
              CHECK (status IN ('new', 'done', 'wontfix')),
  review_note TEXT,
  reviewed_at TEXT
);

CREATE INDEX IF NOT EXISTS reports_status ON reports (status, created_at);
CREATE INDEX IF NOT EXISTS reports_ip_day ON reports (ip_hash);
