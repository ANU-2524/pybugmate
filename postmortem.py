def postmortem_excepthook(exc_type, exc_val, exc_tb):
    import sys
    tb = exc_tb
    while tb.tb_next is not None:
        tb = tb.tb_next
    frame = tb.tb_frame

    try:
        from IPython.terminal.embed import InteractiveShellEmbed
        from traitlets.config import Config
        c = Config()
        c.TerminalInteractiveShell.banner1 = ""  # No banner
        print("[PyBugMate] Dropping you into the crash shell. Inspect and fix, then exit().\n")
        shell = InteractiveShellEmbed(config=c, user_ns=frame.f_locals)
        shell.mainloop()
    except Exception:
        import code
        print("[PyBugMate] Dropping you into classic Python shell at crash. Type exit() or Ctrl-D to exit.\n")
        code.interact(local=frame.f_locals)

def enable_postmortem() :
    import sys
    sys.excepthook = postmortem_excepthook
        
        
    
    