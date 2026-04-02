class PiiScrubber
  SAFE_WORDS = %w[
    monday tuesday wednesday thursday friday saturday sunday
    january february march april june july august september october november december
    south north east west living bedroom classroom bathroom kitchen playground
  ].freeze

  PATTERNS = [
    { label: "phone",  regex: /(\+?1?\s?)?(\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4})/,  replacement: "555-000-0000" },
    { label: "email",  regex: /[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/,    replacement: "student@example.com" },
    { label: "ssn",    regex: /\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b/,                      replacement: "XXX-XX-XXXX" },
    { label: "date",   regex: %r{\b(0?[1-9]|1[0-2])[/\-](0?[1-9]|[12]\d|3[01])[/\-](\d{2}|\d{4})\b}, replacement: "a date" },
    { label: "id",     regex: /\b\d{6,}\b/,                                            replacement: "XXXXXXXX" },
  ].freeze

  NAME_REGEX = /(?<![.!?\n])\b([A-Z][a-z]{1,15})(\s[A-Z][a-z]{1,15}){1,2}\b/

  # Returns [scrubbed_text, detected_labels]
  def self.scrub(text)
    return [text, []] if text.blank?

    scrubbed = text.dup
    detected = []

    PATTERNS.each do |p|
      if scrubbed.match?(p[:regex])
        detected << p[:label]
        scrubbed.gsub!(p[:regex], p[:replacement])
      end
    end

    scrubbed.gsub!(NAME_REGEX) do |match|
      words = match.downcase.split
      if (words & SAFE_WORDS).any?
        match
      else
        detected << "name"
        "the student"
      end
    end

    [scrubbed, detected.uniq]
  end
end
