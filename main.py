# -*- coding: utf-8 -*-
"""
SwasthyaGuide - Main Entry Point
A multilingual healthcare assistant for accessible health guidance in India
"""

from src.chatbot import SwasthyaGuide


def main():
    """Main entry point for the application"""
    chatbot = SwasthyaGuide()
    chatbot.run_cli()


if __name__ == "__main__":
    main()
