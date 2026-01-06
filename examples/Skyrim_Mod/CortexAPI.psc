Scriptname CortexAPI Hidden
{
    Project Cortex - Skyrim Integration
    
    This script provides an interface to communicate with
    the Cortex AI server for intelligent NPC dialogue.
    
    Requirements:
      - Cortex.exe running (port 8000)
      - PapyrusHTTP or similar SKSE plugin for HTTP requests
      
    Author: Project Cortex
    License: MIT
}

; ============================================
; Configuration
; ============================================

String Property CORTEX_URL = "http://127.0.0.1:8000" AutoReadOnly

; ============================================
; Core API Functions
; ============================================

; Send a chat message to Cortex and get NPC response
; @param message - Player's dialogue
; @param speakerName - Player or NPC name
; @return JSON string with reply, emotion, resonance
String Function Chat(String message, String speakerName = "Dragonborn") Global
    String jsonBody = "{\"text\": \"" + message + "\", \"speaker\": \"" + speakerName + "\"}"
    String response = HTTPPost(CORTEX_URL + "/chat", jsonBody)
    return response
EndFunction

; Inject game context into Cortex
; @param location - Current location name
; @param timeOfDay - morning/afternoon/evening/night
; @param weather - clear/rain/snow/storm
Function InjectContext(String location, String timeOfDay, String weather) Global
    String jsonBody = "{\"info\": {"
    jsonBody += "\"location\": \"" + location + "\","
    jsonBody += "\"time\": \"" + timeOfDay + "\","
    jsonBody += "\"weather\": \"" + weather + "\""
    jsonBody += "}}"
    HTTPPost(CORTEX_URL + "/inject", jsonBody)
EndFunction

; Reset NPC memory
Function ForgetAll() Global
    HTTPPost(CORTEX_URL + "/forget", "{}")
EndFunction

; ============================================
; Helper Functions (Requires SKSE HTTP Plugin)
; ============================================

; Placeholder - Replace with actual HTTP plugin call
String Function HTTPPost(String url, String body) Global
    ; This needs to be implemented with your HTTP plugin
    ; Example with PapyrusHTTP:
    ; return PapyrusHTTP.Post(url, body, "application/json")
    
    Debug.Trace("[Cortex] POST " + url)
    return "{\"reply\": \"Greetings, traveler.\", \"emotion\": \"neutral\"}"
EndFunction

; ============================================
; JSON Parsing Helpers
; ============================================

; Extract "reply" field from JSON response
String Function GetReply(String jsonResponse) Global
    ; Simple JSON parsing (for production, use a proper JSON library)
    Int startIndex = StringUtil.Find(jsonResponse, "\"reply\": \"") + 10
    Int endIndex = StringUtil.Find(jsonResponse, "\",", startIndex)
    return StringUtil.Substring(jsonResponse, startIndex, endIndex - startIndex)
EndFunction

; Extract "emotion" field from JSON response
String Function GetEmotion(String jsonResponse) Global
    Int startIndex = StringUtil.Find(jsonResponse, "\"emotion\": \"") + 12
    Int endIndex = StringUtil.Find(jsonResponse, "\"", startIndex)
    return StringUtil.Substring(jsonResponse, startIndex, endIndex - startIndex)
EndFunction
