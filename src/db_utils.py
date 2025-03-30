import sqlite3


def init_db():
    """Initialize the SQLite database and create tables if they don't exist."""
    conn = sqlite3.connect("./db/chat_conversations.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id TEXT,  
        user_id TEXT,          
        role TEXT,             
        content TEXT,          
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )"""
    )
    conn.commit()
    conn.close()


def load_conversation_ids():
    """
    Load all unique conversation IDs from the database.

    Returns:
    dict: A dictionary of conversation IDs with empty list as placeholder.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect("./db/chat_conversations.db")
        cursor = conn.cursor()

        # Query to get unique conversation IDs
        cursor.execute(
            """
            SELECT DISTINCT conversation_id 
            FROM chat_messages 
            ORDER BY conversation_id
        """
        )

        # Fetch all conversation IDs
        conversations = {row[0]: [] for row in cursor.fetchall()}

        conn.close()
        return conversations

    except sqlite3.Error as e:
        print(f"Database error when loading conversation IDs: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error when loading conversation IDs: {e}")
        return {}


def delete_conversation(conversation_id):
    """Delete a conversation from the database."""
    conn = sqlite3.connect("./db/chat_conversations.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    DELETE FROM chat_messages 
    WHERE conversation_id = ?
    """,
        (conversation_id,),
    )
    conn.commit()
    conn.close()


def save_message(conversation_id, role, content):
    """Save a message to the database."""
    conn = sqlite3.connect("./db/chat_conversations.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    INSERT INTO chat_messages (conversation_id, user_id, role, content) 
    VALUES (?, ?, ?, ?)
    """,
        (conversation_id, "user", role, content),
    )
    conn.commit()
    conn.close()


def get_conversation_history(conversation_id):
    """Retrieve conversation history for a given conversation ID."""
    conn = sqlite3.connect("./db/chat_conversations.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    SELECT role, content 
    FROM chat_messages 
    WHERE conversation_id = ? 
    ORDER BY timestamp
    """,
        (conversation_id,),
    )
    history = cursor.fetchall()
    conn.close()
    return [{"role": role, "content": content} for role, content in history]
