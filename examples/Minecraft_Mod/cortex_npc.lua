-- ============================================
-- Cortex NPC Integration for Minecraft
-- ============================================
-- 
-- This example shows how to integrate Project Cortex
-- with a Minecraft mod using ComputerCraft or similar
-- Lua-based mod.
--
-- Requirements:
--   - Cortex.exe running on the same machine
--   - HTTP API enabled in mod config
--
-- Author: Project Cortex
-- License: MIT
-- ============================================

local CORTEX_URL = "http://127.0.0.1:8000"

-- ============================================
-- Core API Functions
-- ============================================

local CortexAPI = {}

--- Send a chat message to Cortex and get NPC response
-- @param message string: Player's message
-- @param speaker string: Player name (optional)
-- @return table: {reply, emotion, resonance, memories_recalled}
function CortexAPI.chat(message, speaker)
    speaker = speaker or "Player"
    
    local response = http.post(
        CORTEX_URL .. "/chat",
        textutils.serialiseJSON({
            text = message,
            speaker = speaker
        }),
        {["Content-Type"] = "application/json"}
    )
    
    if response then
        local body = response.readAll()
        response.close()
        return textutils.unserialiseJSON(body)
    else
        return {reply = "...", emotion = "confused", resonance = 0}
    end
end

--- Inject game context into Cortex
-- @param context table: Game state information
function CortexAPI.inject(context)
    http.post(
        CORTEX_URL .. "/inject",
        textutils.serialiseJSON({info = context}),
        {["Content-Type"] = "application/json"}
    )
end

--- Reset NPC memory
function CortexAPI.forget()
    http.post(CORTEX_URL .. "/forget", "{}", {["Content-Type"] = "application/json"})
end

-- ============================================
-- Example Usage
-- ============================================

-- Example 1: Simple conversation
local function simpleConversation()
    print("=== Simple Conversation ===")
    
    local result = CortexAPI.chat("Hello! What's your name?", "Steve")
    
    print("NPC: " .. result.reply)
    print("Emotion: " .. result.emotion)
    print("Resonance: " .. result.resonance .. "%")
end

-- Example 2: Context-aware conversation
local function contextAwareConversation()
    print("=== Context-Aware Conversation ===")
    
    -- Inject current game state
    CortexAPI.inject({
        location = "Village",
        time = "night",
        weather = "rain",
        player_health = 15,
        nearby_mobs = {"zombie", "skeleton"}
    })
    
    -- Now the NPC knows the situation
    local result = CortexAPI.chat("Is it safe here?", "Steve")
    
    print("NPC: " .. result.reply)
    -- Expected: The NPC might warn about nearby mobs or the dangerous night
end

-- Example 3: Memory recall
local function memoryRecallExample()
    print("=== Memory Recall ===")
    
    -- First conversation
    CortexAPI.chat("My name is Alex and I love building.", "Alex")
    
    -- Later...
    local result = CortexAPI.chat("Do you remember what I like to do?", "Alex")
    
    print("NPC: " .. result.reply)
    
    -- Check recalled memories
    if #result.memories_recalled > 0 then
        print("Recalled memory: " .. result.memories_recalled[1].text)
        print("Similarity: " .. result.memories_recalled[1].similarity)
    end
end

-- ============================================
-- Integration with NPC Entity
-- ============================================

local NPCController = {}

function NPCController.new(npcName)
    local self = {
        name = npcName,
        lastEmotion = "neutral"
    }
    
    function self:speak(playerMessage, playerName)
        local result = CortexAPI.chat(playerMessage, playerName)
        
        -- Update NPC state based on emotion
        self.lastEmotion = result.emotion
        
        -- Display response (implement based on your mod)
        -- Example: Show chat bubble, play animation
        self:displayMessage(result.reply)
        self:playEmotionAnimation(result.emotion)
        
        return result
    end
    
    function self:displayMessage(message)
        print("[" .. self.name .. "]: " .. message)
    end
    
    function self:playEmotionAnimation(emotion)
        -- Map emotions to animations
        local animations = {
            confident = "nod",
            neutral = "idle",
            uncertain = "think",
            confused = "scratch_head"
        }
        print("  *" .. (animations[emotion] or "idle") .. "*")
    end
    
    return self
end

-- ============================================
-- Run Examples
-- ============================================

print("Project Cortex - Minecraft Integration Example")
print("=" .. string.rep("=", 45))

-- Make sure Cortex.exe is running!
simpleConversation()
print("")
contextAwareConversation()
print("")
memoryRecallExample()
print("")

-- Create an NPC and interact
local villager = NPCController.new("Villager Bob")
villager:speak("Hello, what do you sell?", "Steve")
