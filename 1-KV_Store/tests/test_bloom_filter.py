from src.log_structured_kvstore.bloom_filter import BloomFilter

class TestBloomFilter:
    def test_add_and_check(self):
        bf = BloomFilter(1000)
        bf.add("test_key")
        assert bf.may_contain("test_key") == True
        assert bf.may_contain("non_existent_key") == False

    def test_false_positive_rate(self):
        bf = BloomFilter(1000)
        for i in range(100):
            bf.add(f"key{i}")

        false_positives = 0
        for i in range(100, 200):
            if bf.may_contain(f"key{i}"):
                false_positives += 1

        # False positive rate should be relatively low
        assert false_positives / 100 < 0.1