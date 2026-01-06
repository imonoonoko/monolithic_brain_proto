Scriptname CortexNPC extends ObjectReference
{
    Example NPC script that uses Cortex for intelligent dialogue.
    
    Attach this script to an NPC and configure their personality
    through the Cortex server's system prompt.
}

; ============================================
; Properties
; ============================================

String Property NPCName = "Villager" Auto
{Display name of this NPC}

Actor Property PlayerRef Auto
{Reference to the player}

; ============================================
; Events
; ============================================

Event OnActivate(ObjectReference akActionRef)
    If akActionRef == PlayerRef
        StartConversation()
    EndIf
EndEvent

; ============================================
; Conversation System
; ============================================

Function StartConversation()
    ; Inject current game context
    InjectGameContext()
    
    ; Get player input (simplified - use dialogue menu in production)
    String playerMessage = "Hello, " + NPCName + "!"
    
    ; Send to Cortex
    String response = CortexAPI.Chat(playerMessage, "Dragonborn")
    
    ; Parse response
    String reply = CortexAPI.GetReply(response)
    String emotion = CortexAPI.GetEmotion(response)
    
    ; Display NPC response
    DisplayResponse(reply, emotion)
EndFunction

Function InjectGameContext()
    ; Get current location
    String locationName = PlayerRef.GetCurrentLocation().GetName()
    
    ; Get time of day
    Float currentHour = GameHour.GetValue()
    String timeOfDay = "day"
    If currentHour < 6.0 || currentHour > 20.0
        timeOfDay = "night"
    EndIf
    
    ; Get weather
    String weather = "clear"
    Weather currentWeather = Weather.GetCurrentWeather()
    If currentWeather.GetClassification() == 2  ; Rainy
        weather = "rain"
    ElseIf currentWeather.GetClassification() == 3  ; Snowy
        weather = "snow"
    EndIf
    
    CortexAPI.InjectContext(locationName, timeOfDay, weather)
EndFunction

Function DisplayResponse(String message, String emotion)
    ; Show dialogue
    Debug.Notification(NPCName + ": " + message)
    
    ; Play emotion-appropriate animation
    PlayEmotionAnim(emotion)
EndFunction

Function PlayEmotionAnim(String emotion)
    Actor selfActor = Self as Actor
    
    If emotion == "confident"
        Debug.SendAnimationEvent(selfActor, "IdleApplaud")
    ElseIf emotion == "uncertain"
        Debug.SendAnimationEvent(selfActor, "IdleScratchHead")
    ElseIf emotion == "confused"
        Debug.SendAnimationEvent(selfActor, "IdleShrug")
    Else
        ; neutral - do nothing special
    EndIf
EndFunction
