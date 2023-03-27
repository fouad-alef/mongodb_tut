class ChatConversation:
    @staticmethod
    async def get_session(session_id: str) -> Optional[ChatSession]:
        # Retrieve a ChatSession document from the database based on the provided session_id
        return await ChatSession.find_one(ChatSession.session_id == session_id)

    @staticmethod
    async def create_session(user_request: UserRequest) -> ChatSession:
        # Create a new ChatSession document in the database with the provided user request information
        session = ChatSession(
            session_id=user_request.context_id,
            user_id=user_request.user_id,
            context_id=user_request.context_id,
            course_id=user_request.course_id,
            activity_id=user_request.activity_id,
            outcome_id=user_request.outcome_id,
        )
        result = await ChatSession.insert_one(session)
        logging.info("New chat session created with session_id : {}".format(session.session_id))
        return session

    @staticmethod
    async def update_session_status(session_id: str, session_status: SessionStatus) -> Optional[ChatSession]:
        # Update the session_status field of an existing ChatSession document in the database
        session = await ChatConversation.get_session(session_id)
        if session:
            session.session_status = session_status
            await session.update()
            logging.info(f"Chat session with session_id : {session.session_id} updated with new session status: {session_status}")
        return session

    @staticmethod
    async def create_conversation(user_request: UserRequest) -> ChatConversation:
        # Check if a ChatSession document already exists in the database for the provided user request
        session = await ChatConversation.get_session(user_request.context_id)
        if session:
            # If the ChatSession document exists, update the session_status field with the new status
            session = await ChatConversation.update_session_status(user_request.context_id, SessionStatus.IN_PROGRESS)
        else:
            # If the ChatSession document does not exist, create a new one with the provided user request information
            session = await ChatConversation.create_session(user_request)
        # Create a new ChatConversation document in the database with the provided user request information and the session information from the matching ChatSession document
        conversation = ChatConversation(
            user_id=user_request.user_id,
            session_id=user_request.context_id,
            remaining_token=session.token_length,
            session_status=SessionStatus.STARTED,
            session_length=session.token_length,
            timestamp=user_request.timestamp,
        )
        result = await ChatConversation.insert_one(conversation)
        logging.info("New chat conversation created for session_id : {user_request.context_id}")
        return conversation