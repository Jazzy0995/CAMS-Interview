# # # crew_engine/crew_main.py
# # from crewai import Crew
# # from crew_engine.agents import build_agents
# # from crew_engine.tasks import build_tasks

# # def build_email_crew(email_content, predicted_category):
# #     email_interpreter, response_writer = build_agents()

# #     interpret_task, compose_task = build_tasks(
# #         email_interpreter,
# #         response_writer,
# #         email_content,         # <-- f-string injection enabled
# #         predicted_category     # <-- injected too
# #     )

# #     crew = Crew(
# #         agents=[email_interpreter, response_writer],
# #         tasks=[interpret_task, compose_task],
# #         verbose=False
# #     )
# #     return crew

# ########################################################################################################
# # crew_engine/crew_main.py
# from crewai import Crew
# from crew_engine.agents import build_agents
# from crew_engine.tasks import build_tasks

# def build_email_crew(email_content, predicted_category):
#     (
#         email_interpreter,
#         response_writer,
#         attachment_selector,
#         attachment_generator
#     ) = build_agents()

#     tasks = build_tasks(
#         email_interpreter,
#         response_writer,
#         attachment_selector,
#         attachment_generator,
#         email_content,
#         predicted_category
#     )

#     crew = Crew(
#         agents=[
#             email_interpreter,
#             response_writer,
#             attachment_selector,
#             attachment_generator
#         ],
#         tasks=list(tasks),
#         verbose=False
#     )
#     return crew
# ########################################################################################################

# # crew_main.py
# from crewai import Crew
# from crew_engine.agents import build_agents
# from crew_engine.tasks import build_tasks

# def build_email_crew(email_content, predicted_category):

#     (
#         email_interpreter,
#         response_writer,
#         attachment_selector,
#         attachment_generator
#     ) = build_agents()

#     tasks = build_tasks(
#         email_interpreter,
#         response_writer,
#         attachment_selector,
#         attachment_generator,
#         email_content,
#         predicted_category
#     )

#     crew = Crew(
#         agents=[
#             email_interpreter,
#             response_writer,
#             attachment_selector,
#             attachment_generator
#         ],
#         tasks=list(tasks),
#         verbose=False
#     )

#     return crew


#######################################################################################################

# crew_main.py
from crewai import Crew
from crew_engine.agents import build_agents
from crew_engine.tasks import build_tasks

def build_email_crew(email_content, predicted_category):

    (
        email_interpreter,
        response_writer,
        attachment_selector,
        attachment_generator
    ) = build_agents()

    tasks = build_tasks(
        email_interpreter,
        response_writer,
        attachment_selector,
        attachment_generator,
        email_content,
        predicted_category
    )

    crew = Crew(
        agents=[
            email_interpreter,
            response_writer,
            attachment_selector,
            attachment_generator
        ],
        tasks=list(tasks),
        verbose=False
    )

    return crew
