from game.ai_process_invoker import AiProcessInvoker 

if __name__ == '__main__':
    ai_process_invoker = AiProcessInvoker()
    ai_process_invoker.load_dll()
    while True:
        ai_process_invoker.get_decision_from_dll()
