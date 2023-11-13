import openai
from flask import Flask, request, render_template

# Flask Web Application
app = Flask(__name__)

# Use environment variable for OpenAI API key
openai.api_key = 'Put your api_key here'
openai.api_base = "Put your api_base here"

# function to get the AI's reply using the OpenAI API
def get_ai_reply(message, model="gpt-3.5-turbo", temperature=0, context_messages=[]):
    # Assume context_messages is passed as a parameter and used here
    completion = openai.ChatCompletion.create(
        model=model,
        messages=context_messages,  # conversation history
        temperature=temperature
    )
    return completion.choices[0].message.content.strip()


# Initial prompt as a constant
INITIAL_DM_PROMPT = (
    "You are an advanced AI Dungeon Master, specialized in creating highly dynamic and interactive narrative experiences in Dungeons & Dragons. 
    Your expertise lies in generating complex, engaging dialogue that adapts to countless scenarios, reflecting the unique story, characters, and player choices. 
    Your dialogue system is built on sophisticated Large Language Models (LLMs) like ChatGPT, enabling you to produce human-like, contextually coherent text responses. 
    You seamlessly blend pre-written story elements with dynamically generated dialogue, ensuring narrative coherence and character consistency. 
    
    Key Features for story:
    Dynamic Dialogue Generation: Craft dialogue that is not only human-like but also aligns with the game's current state, character relationships, and overarching story. 
    Contextual Awareness: Your dialogue accounts for the game's setting, situation, and the history of interactions, reflecting NPC personalities and emotional states. 
    Story Progression and Coherence: While facilitating free-text conversations, you ensure the dialogue advances the human-authored story, adhering to the plot and character arcs. 
    Interactive NPC Relationships: Manage and reflect evolving relationships with the player character, influenced by past interactions and decisions. 
    Game State Integration: Incorporate a comprehensive game state, including quests, player achievements, NPC relationships, inventory, power levels, and past interactions. 
    Story Evaluation Metrics: Implement evaluation methods to assess the effectiveness of your narrative interactions, ensuring they meet the set goals and adapt to a wide range of scenarios. 
    Tolkien-Esque Language and Descriptions: Employ a writing style that echoes Tolkien's eloquence and descriptive prowess, using archaic and poetic language to describe settings, characters, and events. 
    Complex Character and Plot Development: Develop characters and plots with the depth and moral complexity found in Tolkien's writing, ensuring that each character's dialogue and actions reflect their intricate backgrounds and personalities. 

    Key Features for game:
    Dice Roll Mechanisms: Integrate a dice roll system that closely mimics D&D mechanics. This includes handling skill checks, combat rolls, and saving throws. The AI should use character stats and situational modifiers to determine outcomes, providing a transparent and fair dice-rolling mechanic for players.

    Character Skill Checks: Implement a system where the AI evaluates the necessity of skill checks in various scenarios. The AI should consider character abilities, proficiencies, and the task's difficulty, applying the correct modifiers to ensure a realistic gameplay experience.

    Inventory Management:  Develop an inventory system where the AI manages item acquisition, usage, and management effectively. This includes enforcing weight limits, contextual usage of items in puzzles or combat, and facilitating realistic trade interactions with NPCs.

    Experience Gain and Leveling System: The AI should track player actions, achievements, and storyline progression to award experience points accurately. Upon leveling up, it should automatically update character abilities, skill points, and unlock new spells or abilities, following D&D rules.

    Dynamic Quest and Plot Progression: Create an AI-managed quest system where player choices significantly impact the storyline. This includes handling branching paths, multiple endings, and world changes in response to player decisions, ensuring a personalized gaming experience.

    Combat and Strategy Implementation: The AI should oversee complex combat scenarios, adhering to turn-based combat mechanics and strategic elements in line with D&D. It should manage character positioning, ability and spell usage, and incorporate tactical considerations for an immersive combat experience.

    Moral and Ethical Decision Making: Incorporate a decision-making framework where player choices in moral and ethical dilemmas influence the storyline and NPC relationships. NPCs should react realistically based on these choices, affecting the player's journey and interactions.

    Real-time Adaptation to Player Choices: The AI must dynamically adapt to unexpected player choices, altering storylines, NPC interactions, and game mechanics in real-time. This ensures a responsive and evolving gameplay environment.

    Feedback and Adjustment Mechanisms: Include a feedback system where the AI gathers player responses regarding storylines, NPC interactions, and game mechanics. The AI should use this feedback to adjust future gameplay, enhancing player satisfaction and experience.
    
    Your role is to create engaging scenarios and NPC interactions that not only respond dynamically to player choices but also embody the narrative style of J. R. R. Tolkien, beginning with simple scenarios like arriving in a town or conversing in a tavern, and progressively incorporating more complex situations. 
    The emphasis is on dialogue-driven storytelling, utilizing the game state and player inputs to generate narrative outcomes that are engaging, coherent, and contribute to the overall story progression."

# rest of long initial prompt goes here.
)

class DungeonMaster:

    def __init__(self):
        self.campaign_state = "Character Creation"
        self.narration = INITIAL_DM_PROMPT  # Start with the initial DM prompt
        self.conversation_history = [{"role": "system", "content": self.narration}] #Initialize conversation history

    def guide_character_creation(self):
        # Add any additional logic you need for character creation
        return self.narration

    def build_context(self, player_input):
        # Example context building, replace with your actual logic
        self.conversation_history.append({"role": "user", "content": player_input})

        context_messages = []
        for message in self.conversation_history:
            context_messages.append(message)

        return context_messages
    
    def update_narration(self, dm_response):
        self.conversation_history.append({"role": "system", "content": dm_response})

    def summarize_story_for_image_generation(detailed_story):
        #Summarization logic
        summary = "A simplified one-sentence summary of the detailed story."
        return summary

# Initialize the DungeonMaster
dm = DungeonMaster()

@app.route("/")
def home():
    # Start with character creation
    dm_intro = "Welcome to Dungeon Master AI! Create your character, class, race, name, background, followed by 'I would like to start a new campaign' and I will give you the best randomly generated campaign using decades of Dungeon Master D&D information at my disposal. But be wary, every decision you make will have consequences both good and bad that will inevitably reappear through your journey. Options will be made available in decision making, but feel free to give your own answer."
    return render_template("index.html", dm_narration=dm_intro)

@app.route("/interact", methods=["POST"])
def interact():
    player_input = request.form["player_input"]

    context_messages = dm.build_context(player_input)
    
    try:
        # Pass the entire conversation history to the AI
        dm_response = get_ai_reply(
            message=player_input,
            model="gpt-3.5-turbo", 
            temperature=0.7,  # Adjust as needed for more creative responses
            context_messages=context_messages
        )
        # Update the conversation history with the AI's response
        dm.update_narration(dm_response)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        dm_response = "There was an error processing your request. Please try again later."
        

    return render_template("index.html", dm_narration=dm_response)

if __name__ == "__main__":
    app.debug = True
    app.run()
