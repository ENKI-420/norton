import type { Message } from "ai"

// Enhanced Interface to Structure AI Response
export interface EnhancedChatResponse {
  sanitizedMessage: string
  quickReplies: string[]
  formattedGenomicData?: string
  usage?: {
    promptTokens: number
    completionTokens: number
    totalTokens: number
  }
}

// Enhanced Sensitive Data Detection (Expanded PHI and Non-PHI)
export function containsSensitiveHealthInfo(message: string): boolean {
  const sensitivePatterns = [
    /\b\d{3}-\d{2}-\d{4}\b/, // SSN
    /\b\d{9}\b/, // MRN
    /\bpatient id\b/i, // Generic "patient id"
    /\bphi\b/i, // PHI
    /\bdate of birth\b/i, // Date of Birth
    /\bphone number\b/i, // Phone number
    /\bemail address\b/i, // Email address
    /\baddress\b/i, // Address
    /\binsurance\b/i, // Insurance
    /\bmedical history\b/i, // Medical history
    /\bmedication\b/i, // Medications
    /\bfamily history\b/i, // Family health history
    /\bgenetic disorder\b/i, // Genetic disorders
    /\bclinical trial\b/i, // Clinical trial identifiers
    /\bresearch data\b/i // Research participation
  ]
  return sensitivePatterns.some((pattern) => pattern.test(message))
}

// Enhanced Sanitization for Compliance
export function sanitizeForHIPAA(message: string): string {
  let sanitizedMessage = message

  if (containsSensitiveHealthInfo(message)) {
    sanitizedMessage = sanitizedMessage.replace(/\b\d{3}-\d{2}-\d{4}\b/, "[REDACTED SSN]")
                                      .replace(/\b\d{9}\b/, "[REDACTED MRN]")
                                      .replace(/\bphi\b/i, "[REDACTED PHI]")
                                      .replace(/\bphone number\b/i, "[REDACTED PHONE]")
                                      .replace(/\bemail address\b/i, "[REDACTED EMAIL]")
                                      .replace(/\baddress\b/i, "[REDACTED ADDRESS]")
                                      .replace(/\binsurance\b/i, "[REDACTED INSURANCE]")
                                      .replace(/\bmedical history\b/i, "[REDACTED MEDICAL HISTORY]")
                                      .replace(/\bmedication\b/i, "[REDACTED MEDICATION]")
                                      .replace(/\bfamily history\b/i, "[REDACTED FAMILY HISTORY]")
                                      .replace(/\bgenetic disorder\b/i, "[REDACTED GENETIC DISORDER]")
                                      .replace(/\bclinical trial\b/i, "[REDACTED CLINICAL TRIAL]")
                                      .replace(/\bresearch data\b/i, "[REDACTED RESEARCH DATA]");

    return sanitizedMessage + " [This message was redacted for HIPAA compliance.]";
  }
  return sanitizedMessage
}

// Advanced Genomic Data Formatting (Dynamic and Scalable)
export function formatGenomicData(data: any): string {
  try {
    // For larger genomic datasets, return as a well-structured object or pretty-printed JSON.
    if (typeof data === "object" && data !== null) {
      return JSON.stringify(data, null, 2); // For structured objects like gene mutations or clinical trials.
    }
    return String(data); // Handle non-structured or string-based data
  } catch (error) {
    console.error("Error formatting genomic data:", error)
    return "Error formatting genomic data";
  }
}

// Context-Aware Quick Reply Generation (Using NLP Context)
export function generateQuickReplySuggestions(message: string, patientData: any): string[] {
  const content = message.toLowerCase()
  
  // Adding personalized replies based on patient data, like history or condition
  if (content.includes("mutation") || content.includes("genomic")) {
    return [
      "Show more details about this mutation",
      "What are the clinical implications?",
      "Compare with normal gene sequence",
      "What genetic tests are available for this mutation?",
      "What are the common mutations associated with this condition?",
      `Can you show how this mutation relates to ${patientData.name}'s health history?`
    ]
  } else if (content.includes("gene") || content.includes("expression")) {
    return [
      "Show expression levels in detail",
      "How does this affect treatment options?",
      "Are there relevant clinical trials?",
      "What gene therapies are available?",
      `What gene therapies could work best for ${patientData.name}'s condition?`,
      "Are there any environmental factors that impact this gene expression?"
    ]
  }
  
  // Default quick replies
  return [
    "Tell me more about this finding",
    "What are the next steps?",
    "How does this compare to normal values?",
    "Are there any treatment implications?",
    "Can you explain this in simpler terms?"
  ]
}import type { Message } from "ai"

// Enhanced Interface to Structure AI Response
export interface EnhancedChatResponse {
  sanitizedMessage: string
  quickReplies: string[]
  formattedGenomicData?: string
  usage?: {
    promptTokens: number
    completionTokens: number
    totalTokens: number
  }
}

// Enhanced Sensitive Data Detection (Expanded PHI and Non-PHI)
export function containsSensitiveHealthInfo(message: string): boolean {
  const sensitivePatterns = [
    /\b\d{3}-\d{2}-\d{4}\b/, // SSN
    /\b\d{9}\b/, // MRN
    /\bpatient id\b/i, // Generic "patient id"
    /\bphi\b/i, // PHI
    /\bdate of birth\b/i, // Date of Birth
    /\bphone number\b/i, // Phone number
    /\bemail address\b/i, // Email address
    /\baddress\b/i, // Address
    /\binsurance\b/i, // Insurance
    /\bmedical history\b/i, // Medical history
    /\bmedication\b/i, // Medications
    /\bfamily history\b/i, // Family health history
    /\bgenetic disorder\b/i, // Genetic disorders
    /\bclinical trial\b/i, // Clinical trial identifiers
    /\bresearch data\b/i // Research participation
  ]
  return sensitivePatterns.some((pattern) => pattern.test(message))
}

// Enhanced Sanitization for Compliance
export function sanitizeForHIPAA(message: string): string {
  let sanitizedMessage = message

  if (containsSensitiveHealthInfo(message)) {
    sanitizedMessage = sanitizedMessage.replace(/\b\d{3}-\d{2}-\d{4}\b/, "[REDACTED SSN]")
                                      .replace(/\b\d{9}\b/, "[REDACTED MRN]")
                                      .replace(/\bphi\b/i, "[REDACTED PHI]")
                                      .replace(/\bphone number\b/i, "[REDACTED PHONE]")
                                      .replace(/\bemail address\b/i, "[REDACTED EMAIL]")
                                      .replace(/\baddress\b/i, "[REDACTED ADDRESS]")
                                      .replace(/\binsurance\b/i, "[REDACTED INSURANCE]")
                                      .replace(/\bmedical history\b/i, "[REDACTED MEDICAL HISTORY]")
                                      .replace(/\bmedication\b/i, "[REDACTED MEDICATION]")
                                      .replace(/\bfamily history\b/i, "[REDACTED FAMILY HISTORY]")
                                      .replace(/\bgenetic disorder\b/i, "[REDACTED GENETIC DISORDER]")
                                      .replace(/\bclinical trial\b/i, "[REDACTED CLINICAL TRIAL]")
                                      .replace(/\bresearch data\b/i, "[REDACTED RESEARCH DATA]");

    return sanitizedMessage + " [This message was redacted for HIPAA compliance.]";
  }
  return sanitizedMessage
}

// Advanced Genomic Data Formatting (Dynamic and Scalable)
export function formatGenomicData(data: any): string {
  try {
    // For larger genomic datasets, return as a well-structured object or pretty-printed JSON.
    if (typeof data === "object" && data !== null) {
      return JSON.stringify(data, null, 2); // For structured objects like gene mutations or clinical trials.
    }
    return String(data); // Handle non-structured or string-based data
  } catch (error) {
    console.error("Error formatting genomic data:", error)
    return "Error formatting genomic data";
  }
}

// Context-Aware Quick Reply Generation (Using NLP Context)
export function generateQuickReplySuggestions(message: string, patientData: any): string[] {
  const content = message.toLowerCase()
  
  // Adding personalized replies based on patient data, like history or condition
  if (content.includes("mutation") || content.includes("genomic")) {
    return [
      "Show more details about this mutation",
      "What are the clinical implications?",
      "Compare with normal gene sequence",
      "What genetic tests are available for this mutation?",
      "What are the common mutations associated with this condition?",
      `Can you show how this mutation relates to ${patientData.name}'s health history?`
    ]
  } else if (content.includes("gene") || content.includes("expression")) {
    return [
      "Show expression levels in detail",
      "How does this affect treatment options?",
      "Are there relevant clinical trials?",
      "What gene therapies are available?",
      `What gene therapies could work best for ${patientData.name}'s condition?`,
      "Are there any environmental factors that impact this gene expression?"
    ]
  }
  
  // Default quick replies
  return [
    "Tell me more about this finding",
    "What are the next steps?",
    "How does this compare to normal values?",
    "Are there any treatment implications?",
    "Can you explain this in simpler terms?"
  ]
}