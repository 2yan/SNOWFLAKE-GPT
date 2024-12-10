# Repository README

## Lambda Setup

1. **Upload Files to AWS Lambda:**

   - Upload `lambda_function.py` and `con.py` to your AWS Lambda function.

2. **Create a Layer with Dependencies:**

   - Include all dependencies, especially for Snowflake.
   - Use [aws_layer_maker](https://github.com/2yan/aws_layer_maker) to create the layer.

---

## GPT Setup

1. **Create a Custom GPT Model:**

   - Copy the contents of `instructions.md` directly into the GPT model setup.

2. **Create a Custom Action:**

   - Copy the contents of `action.md` directly into the action setup.

---

## Notes

- **Authentication:**
  - You will need to implement your own authentication system.

---

### License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

### Contributions

Feel free to submit pull requests or open issues for any improvements.

### Contact

For questions or support, please contact me. 
